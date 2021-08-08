# Author: Matthew Trotter
# Copyright 2021

from camera import Camera
from pathlib import Path
import tempfile
from typing import List
from uploader import Uploader
from updater import Updater

import logging
import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('node')


class ResponseParser:
    def __init__(self, local_storage_dir: Path) -> None:
        self.camera = Camera(local_storage_dir=local_storage_dir)
        self.uploader = Uploader()
        self.updater = Updater()

    def parse_pictures(self, responses: List):
        """Parse the responses from SQS RemoteCameraPictures queue

        Parameters
        ----------
        responses : List
            Responses from SQS service client.receive_message() command.
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.receive_message 
        """
        if responses:
            for response in responses:
                key = response.body
                picture = self.camera.take_picture()
                self.uploader.upload(picture, key)
    
    def parse_update(self, responses: List):
        """Parse the responses from SQS RemoteCameraUpdates queue

        Parameters
        ----------
        responses : Dict or List
            Responses from SQS service client.receive_message() command.
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.receive_message 
        """
        if responses:
            for response in responses:
                url = response.body
                self.updater.update(url)
