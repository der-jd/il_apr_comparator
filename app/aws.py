import boto3


def get_parameter_value(parameter_name: str | None) -> str:
    if parameter_name is None:
        return ""

    client = boto3.client('ssm')
    response = client.get_parameter(Name = parameter_name)
    value = response['Parameter']['Value']
    return value

def send_sns_notification(topic_arn: str, subject: str, message: str) -> None:
    client = boto3.client('sns')
    print(f"Publish message to topic '{topic_arn}'...")
    client.publish(TopicArn = topic_arn, Subject = subject, Message = message)
