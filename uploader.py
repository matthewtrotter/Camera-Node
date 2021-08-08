# Author: Matthew Trotter
# Copyright 2021

import boto3
import hashlib
from pathlib import Path

import logging
import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('uploader')


class Uploader:
    def __init__(self) -> None:
        self.s3 = boto3.resource('s3')
        self.bucket = self.s3.Bucket('remotecamerapics')

    def upload(self, file: Path, key: str):
        """Upload the file to the URL

        Parameters
        ----------
        file : Path
            File to upload
        key : str
            Key of the file on the S3 bucket (e.g. file.jpg)
        """
        with open(file, 'rb') as fp:
            body = fp.read()
            contentMD5 = hashlib.md5(body).hexdigest()
            print(contentMD5)
            self.bucket.put_object(
                ACL='public-read',
                Body=body,
                ContentType='jpg',
                Key=key
                )
            logger.info(f'Uploaded file {file} to {self.bucket} S3 bucket with key {key}')
