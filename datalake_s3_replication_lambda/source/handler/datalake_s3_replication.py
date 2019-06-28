import json
import os
import logging
from urllib.parse import unquote_plus
from source.constants.source_mapping import source_to_destination_mapping
from source.constants.constants import DeletionStatus, EventType
from source.exceptions.datalake_exceptions import SourceBucketLookupException, EventTypeException
from source.client import aws_client

logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s, %(asctime)s, %(module)s, %(message)s"
)

REGION = os.environ.get('region_name', 'ca-central-1')
SQS_QUEUE_URL = os.environ.get('sqs_queue_url', '')
SQS_PROCESS_ENABLED = os.environ.get('sqs_process_enabled', False)
NUM_OF_SQS_MESSAGE_TO_PROCESS = os.environ.get('num_of_sqs_messages_to_process', 10)


def lambda_handler(event, context):
    try:
        event_type = get_event_type(event)
        if event_type == EventType.S3_NOTIFICATION.value:
            s3_event = event['Records'][0]['s3']
            source_bucket = s3_event['bucket']['name']
            source_key = unquote_plus(s3_event['object']['key'], encoding='utf-8')
        elif event_type == EventType.SNS_NOTIFICATION.value:
            s3_event = json.loads(event['Records'][0]['Sns']['Message'])
            source_bucket = s3_event['Records'][0]['s3']['bucket']['name']
            source_key = unquote_plus(s3_event['Records'][0]['s3']['object']['key'], encoding='utf-8')

        destination_bucket, delete_source_file = get_destination_bucket(source_bucket)
        # copy object from source bucket to destination bucket
        logger.info("copy {source_bucket}/{source_key} to {destination_bucket}/{destination_key}".format(source_bucket=source_bucket, source_key=source_key, destination_bucket=destination_bucket, destination_key=source_key))
        aws_client.copy_s3(source_bucket=source_bucket, source_key=source_key, destination_bucket=destination_bucket, destination_key=source_key)

        if delete_source_file:
            logger.info('delete {source_bucket}/{source_key}'.format(source_bucket=source_bucket, source_key=source_key))
            delete_status = delete_source_object(source_bucket=source_bucket, source_key=source_key)
            logger.info('delete status: {}'.format(delete_status))
        if SQS_PROCESS_ENABLED == 'true':
            process_sqs()
    except Exception as e:
        logger.error(e)
        raise e


def get_event_type(event):
    try:
        s3_event = event['Records'][0]['s3']
        event_type = EventType.S3_NOTIFICATION.value
    except KeyError:
        try:
            s3_event = event['Records'][0]['Sns']
            event_type = EventType.SNS_NOTIFICATION.value
        except KeyError:
            raise EventTypeException('Event type not recognized for event: {}'.format(event))
    return event_type


def get_destination_bucket(source_bucket):
    source_bucket = source_bucket
    source_destination = source_to_destination_mapping.get(source_bucket)
    if not source_destination:
        raise SourceBucketLookupException('No source bucket mapping found for source bucket {}'.format(source_bucket))

    destination_bucket = source_destination.destination_bucket
    delete_source_file = source_destination.delete_source_file
    logger.info("destination bucket for source bucket {source_bucket} is: {destination_bucket}".format(source_bucket=source_bucket, destination_bucket=destination_bucket))
    logger.info("delete source file after copy is: {}".format(delete_source_file))
    return destination_bucket, delete_source_file


def delete_source_object(source_bucket, source_key):
    if not aws_client.check_from_s3(source_bucket, source_key):
        delete_status = DeletionStatus.ABORT.value
        return delete_status

    aws_client.delete_object_from_s3(source_bucket, source_key)

    if aws_client.check_from_s3(source_bucket, source_key):
        delete_status = DeletionStatus.FAIL.value
    else:
        delete_status = DeletionStatus.SUCCESS.value
    return delete_status


def process_sqs():
    for _ in range(int(NUM_OF_SQS_MESSAGE_TO_PROCESS)):
        try:
            response = aws_client.receive_sqs_message()

            if not is_message_in_queue(response):
                return

            message_response = json.loads(response['Messages'][0]['Body'])  # convert to json since value is in string
            event_type = get_event_type(message_response)
            if event_type == EventType.S3_NOTIFICATION.value:
                s3_event = message_response['Records'][0]['s3']
                source_bucket = s3_event['bucket']['name']
                source_key = unquote_plus(s3_event['object']['key'], encoding='utf-8')
            elif event_type == EventType.SNS_NOTIFICATION.value:
                s3_event = json.loads(message_response['Records'][0]['Sns']['Message'])
                source_bucket = s3_event['Records'][0]['s3']['bucket']['name']
                source_key = unquote_plus(s3_event['Records'][0]['s3']['object']['key'], encoding='utf-8')

            destination_bucket, delete_source_file = get_destination_bucket(source_bucket)
            # copy object from source bucket to destination bucket
            logger.info("copy {source_bucket}/{source_key} to {destination_bucket}/{destination_key}".format(
                source_bucket=source_bucket, source_key=source_key, destination_bucket=destination_bucket,
                destination_key=source_key))
            aws_client.copy_s3(source_bucket=source_bucket, source_key=source_key,
                               destination_bucket=destination_bucket, destination_key=source_key)

            if delete_source_file:
                logger.info(
                    'delete {source_bucket}/{source_key}'.format(source_bucket=source_bucket, source_key=source_key))
                delete_status = delete_source_object(source_bucket=source_bucket, source_key=source_key)
                logger.info('delete status: {}'.format(delete_status))
        except Exception as e:
            logger.error(e)
            raise e
        finally:
            if is_message_in_queue(response):
                aws_client.delete_sqs_message(response)


def is_message_in_queue(response):
    try:
        return True if response.get('Messages', None) is not None else False
    except Exception:
        return False