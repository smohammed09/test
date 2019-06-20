import urllib.request, urllib.parse, urllib.error
import boto3
import ast
import json
import os
print('Loading function')

s3 = boto3.client('s3')

def lambda_handler(event, context):
    sns_message = ast.literal_eval(event['Records'][0]['Sns']['Message'])
    target_bucket = os.environ['destination_value']
    source_bucket = str(sns_message['Records'][0]['s3']['bucket']['name'])
    key = str(urllib.parse.unquote_plus(sns_message['Records'][0]['s3']['object']['key']))
    copy_source = {'Bucket':source_bucket, 'Key':key}
    print("Copying %s from bucket %s to bucket %s ..." % (key, source_bucket, target_bucket))
    s3.copy(Bucket=target_bucket, Key=key, CopySource=copy_source)
