import boto3
import os
import json

client = boto3.client("sqs", region_name="ap-northeast-1")

SQS_URL = os.environ.get("WORKER_QUEUE_URL")


def send_msg(msg_data):
    return client.send_message(
        QueueUrl=SQS_URL,
        MessageBody=json.dumps(msg_data),
    )
