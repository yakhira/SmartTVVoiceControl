import boto3
import pickle
import json

from base64 import b64encode

class SmartTV(object):
    def __init__(self, queue_arn):
        region_name = queue_arn.split(":")[3]
        queue_name = queue_arn.split(":")[5]

        sqs = boto3.client(
            service_name='sqs',
            endpoint_url=f'https://sqs.{region_name}.amazonaws.com',
            region_name=region_name
        )
        self.__queue = boto3.resource('sqs', region_name=region_name).Queue(
            sqs.get_queue_url(QueueName=queue_name).get('QueueUrl')
        )

    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            self.__send_message(name, kwargs)
        return wrapper
    
    def wait_for_response(self):
        while True:
            messages = self.__queue.receive_messages(
                AttributeNames=[
                    'SentTimestamp'
                ],
                MaxNumberOfMessages=1,
                MessageAttributeNames=[
                    'All'
                ],
                VisibilityTimeout=0,
                WaitTimeSeconds=20
            )

            for message in messages:
                message_body = message.body
                message.delete()
            return message_body

    def __send_message(self, command, kwargs={}):
        self.__queue.send_message(
            DelaySeconds=0,
            MessageBody=json.dumps(
                {
                    'name': command,
                    'args': kwargs
                }
            )
        )