import boto3


def get_parameter_value(parameter_name: str) -> str:
    client = boto3.client('ssm')
    response = client.get_parameter(Name = parameter_name)
    value = response['Parameter']['Value']
    return value
