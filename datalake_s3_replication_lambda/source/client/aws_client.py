import os
import logging
import boto3
from botocore import exceptions as BotoCoreExceptions
from source.exceptions.datalake_exceptions import FileNotFoundException


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
NoSuchKey_ERROR_ALARM_ENABLED = os.environ.get('NoSuchKey_error_alarm_enabled', 'true')

s3 = boto3.resource('s3', region_name=REGION)
s3_client = boto3.client('s3', region_name=REGION)
sqs_client = boto3.client('sqs', region_name=REGION)


# S3 operations
def copy_s3(source_bucket, source_key, destination_bucket, destination_key):
    try:
        copy_source = {
            'Bucket': source_bucket,
            'Key': source_key
        }
        s3.meta.client.copy_object(Bucket=destination_bucket,
                                   CopySource=copy_source,
                                   Key=destination_key,
                                   ServerSideEncryption='AES256',
                                   ACL='bucket-owner-full-control'
                                   )
    except s3.meta.client.exceptions.NoSuchKey as e:
        if NoSuchKey_ERROR_ALARM_ENABLED == 'true':
            msg = 'copy {source_bucket}/{source_key}. An error occurred (NoSuchKey) when calling the CopyObject operation: The specified key does not exist.' \
                .format(source_bucket=source_bucket, source_key=source_key)
            raise FileNotFoundException(msg)
        else:
            logger.warning('copy {source_bucket}/{source_key}. {error_message}'.format(source_bucket=source_bucket,
                                                                                        source_key=source_key,
                                                                                        error_message=e))
    except BotoCoreExceptions.ClientError as e:
        logger.error(e.response)
        raise e


def check_from_s3(bucket, file_name):
    try:
        s3.Object(bucket, file_name).load()
        return True
    except BotoCoreExceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise e


def delete_object_from_s3(bucket, key):
    try:
        response = s3_client.delete_objects(
            Bucket=bucket,
            Delete={
                'Objects': [
                    {
                        'Key': key,
                    },
                ],
            }
        )
    except BotoCoreExceptions.ClientError as e:
        logger.error(e.response)
        raise e
    return response


# SQS Operations
def receive_sqs_message():
    try:
        response = sqs_client.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            AttributeNames=['All'],
            MaxNumberOfMessages=1
        )
    except BotoCoreExceptions.ClientError as e:
        logger.error(e.response)
        raise e
    return response


def delete_sqs_message(response):
    try:
        receipt_handle = response['Messages'][0]['ReceiptHandle']
        deletion_response = sqs_client.delete_message(
            QueueUrl=SQS_QUEUE_URL, ReceiptHandle=receipt_handle
        )

        if deletion_response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise RuntimeError(
                "Failed to delete messages: response={deletion_response}"
                    .format(deletion_response=deletion_response))

        logger.info("SQS message delete successful! - ReceiptHandle: {}".format(receipt_handle))
    except Exception as e:
        logger.error(e)
