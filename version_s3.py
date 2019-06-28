"""
List all S3 object versions
"""

import os
from boto.s3.connection import S3Connection

print '--- Connecting to S3'
c = S3Connection(aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

print '--- Selecting the bucket'
bucket = c.get_bucket('...')

versions = bucket.list()
#versions = bucket.list(prefix='')

print '--- List all bucket key versions'
for version in versions:
    print version
