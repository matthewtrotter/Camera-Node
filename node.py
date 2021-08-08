# Author: Matthew Trotter
# Copyright 2021


from response_parser import ResponseParser
import tempfile
import time
from typing import List

import boto3
sqs = boto3.resource('sqs')
sqs_client = boto3.client('sqs')
from botocore.exceptions import ClientError

import logging
import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('node')
print(logger)
# logger.setLevel(logging.INFO)

def delete_messages(messages: List):
    for message in messages:
        sqs_client.delete_message(
            QueueUrl=message.queue_url,
            ReceiptHandle=message.receipt_handle
        )

def receive_messages(queue, max_number, wait_time):
    """
    Receive a batch of messages in a single request from an SQS queue.

    Usage is shown in usage_demo at the end of this module.

    :param queue: The queue from which to receive messages.
    :param max_number: The maximum number of messages to receive. The actual number
                       of messages received might be less.
    :param wait_time: The maximum time to wait (in seconds) before returning. When
                      this number is greater than zero, long polling is used. This
                      can result in reduced costs and fewer false empty responses.
    :return: The list of Message objects received. These each contain the body
             of the message and metadata and custom attributes.
    """
    try:
        messages = queue.receive_messages(
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=max_number,
            WaitTimeSeconds=wait_time
        )
        for msg in messages:
            logger.info("Received message: %s: %s", msg.message_id, msg.body)
    except ClientError as error:
        logger.exception("Couldn't receive messages from queue: %s", queue)
        raise error
    else:
        return messages


def main():
    logger.info('Starting up.')
    local_storage_dir = tempfile.TemporaryDirectory()
    res_parser = ResponseParser(local_storage_dir=local_storage_dir.name)
    sleeptime = 2
    rcpics_queue = sqs.get_queue_by_name(QueueName='RemoteCameraPictures')
    rcupdates_queue = sqs.get_queue_by_name(QueueName='RemoteCameraUpdates')
    while True:
        # Receive from RemoteCameraPictures
        responses = receive_messages(rcpics_queue, 1, 1)
        res_parser.parse_pictures(responses)
        delete_messages(responses)

        # Receive from RemoteCameraUpdates
        responses = receive_messages(rcupdates_queue, 1, 1)
        res_parser.parse_update(responses)
        delete_messages(responses)

        logger.info(f'Sleeping for {sleeptime} seconds...')
        time.sleep(sleeptime)

if __name__ == '__main__':
    main()