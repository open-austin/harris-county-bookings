import json

import boto3

__all__ = ['S3Publisher']


class S3Publisher(object):
    def __init__(self, bucket_info):
        self._s3 = boto3.client('s3')
        self._bucket = bucket_info['bucket']
        self._key_prefix = bucket_info['key']

    def publish(self, key_part, data):
        key = '{}/{}'.format(self._key_prefix, key_part)
        self._s3.put_object(Body=data, Bucket=self._bucket, Key=key)
        return 's3://{}/{}'.format(self._bucket, key)
