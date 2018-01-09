import json

import boto3

__all__ = ['S3Publisher']


class S3Publisher(object):
    def __init__(self, bucket_info):
        self._s3 = boto3.client('s3')
        self._bucket = bucket_info['bucket']
        self._key_prefix = bucket_info['key']

    def publish(self, key_part, data):
        self._s3.upload_fileobj(data, self._bucket, self._key_prefix + key_part)
        return 's3://' + self._bucket + self._key_prefix + key_part
