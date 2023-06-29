import os
import json

import boto3


def get_parameter_value(parameter_name: str) -> str:
    client = boto3.client('ssm')
    response = client.get_parameter(Name = parameter_name)
    value = response['Parameter']['Value']
    return value

def send_sns_notification(message: dict) -> None:
    client = boto3.client('sns')
    topic_arn = get_parameter_value(os.environ.get('SNS_TOPIC')) # pyright: ignore [reportGeneralTypeIssues]
    client.publish(TopicArn = topic_arn, Message = json.dumps(message))
