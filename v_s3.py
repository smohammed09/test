import boto3
import re
s3 = boto3.resource('s3')
client = boto3.client('s3')
bucket = s3.Bucket('dev-shah-test-1')
files_from_apollo = []
files = {}
duplicate_files = {}
for my_bucket_object in bucket.objects.all():
    files_from_apollo.append(my_bucket_object)


versions = bucket.list()
#versions = bucket.list(prefix='')

print '--- List all bucket key versions'
for version in versions:
    print version
