import json

import boto3


PARAMETER_STORE_KEY_SNS_TOPIC_NAME = "il-apr-comparator/sns-topic-name"
PARAMETER_STORE_KEY_SNS_TOPIC_REGION = "il-apr-comparator/sns-topic-region"
PARAMETER_STORE_KEY_MAIL_ADDRESS = "il-apr-comparator/mail-address"


def get_parameter_value(parameter_name: str) -> str:
    client = boto3.client('ssm')
    response = client.get_parameter(Name = parameter_name)
    value = response['Parameter']['Value']
    return value


# TODO implement mail dispatch for notification about comparison # pylint: disable = fixme
def send_mail(event, data):
    sns_topic_name = get_parameter_value(PARAMETER_STORE_KEY_SNS_TOPIC_NAME)
    sns_topic_region = get_parameter_value(PARAMETER_STORE_KEY_SNS_TOPIC_REGION)
    mail_address = get_parameter_value(PARAMETER_STORE_KEY_MAIL_ADDRESS)
    message = f"Impermanent Loss and APR for the last 30 days: {data}"

    ses = boto3.client('ses')
    response = ses.publish(
        TopicArn = f"arn:aws:sns:{sns_topic_region}:{event.requestContext.accountId}:{sns_topic_name}",
        Message = message,
        Subject = "Impermanent Loss to APR comparator",
        MessageAttributes = {
            'Email': {
                'DataType': 'String',
                'StringValue': mail_address
            }
        }
    )

    if response.status_code != 200:
        raise RuntimeError("ERROR: Call to AWS SNS failed!")

    return {
        'statusCode': response.status_code,
        'body': json.dumps('Email sent successfully')
    }
