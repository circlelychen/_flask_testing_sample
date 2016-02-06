import boto
from boto.s3.key import Key
from flask import current_app

class s3_api(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def save(self):
        current_app.logger.info("AWS_ACCESS_KEY_ID: {0}".format(current_app.config.get("AWS_ACCESS_KEY_ID")))
        current_app.logger.info("AWS_SECRET_ACCESS_KEY: {0}".format(current_app.config.get("AWS_SECRET_ACCESS_KEY")))
        conn = boto.connect_s3(current_app.config.get("AWS_ACCESS_KEY_ID"),
                               current_app.config.get("AWS_SECRET_ACCESS_KEY"))
        nonexistent = conn.lookup(current_app.config.get('S3_BUCKET_NAME'))
        if not nonexistent:
            bucket = conn.create_bucket(current_app.config.get('S3_BUCKET_NAME'))
        bucket = conn.get_bucket(current_app.config.get('S3_BUCKET_NAME'))
        k = Key(bucket)
        k.key = self.name
        k.set_contents_from_string(self.value)
