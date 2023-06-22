import os

import boto3


def get_parameter_value(parameter_name: str) -> str:
    client = boto3.client('ssm', region_name = os.environ.get('AWS_REGION_OF_PARAMETER_STORE'))
    response = client.get_parameter(Name = parameter_name)
    value = response['Parameter']['Value']
    return value
