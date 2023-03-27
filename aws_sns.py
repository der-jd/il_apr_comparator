#!/usr/bin/env python3

import json

import boto3


PARAMETER_STORE_KEY_SNS_TOPIC_NAME = "il-apr-comparator/sns-topic-name"
PARAMETER_STORE_KEY_SNS_TOPIC_REGION = "il-apr-comparator/sns-topic-region"
PARAMETER_STORE_KEY_MAIL_ADDRESS = "il-apr-comparator/mail-address"


def send_mail(event, data):
    ssm = boto3.client('ssm')
    sns_topic_name = ssm.get_parameters(Name = [PARAMETER_STORE_KEY_SNS_TOPIC_NAME])['Parameters'][0]['Value']
    sns_topic_region = ssm.get_parameters(Name = [PARAMETER_STORE_KEY_SNS_TOPIC_REGION])['Parameters'][0]['Value']
    mail_address = ssm.get_parameters(Name = [PARAMETER_STORE_KEY_MAIL_ADDRESS])['Parameters'][0]['Value']
    message = f"Impermanent Loss and APR for the last 30 days: {data}" # TODO update mail message

    sns = boto3.client('sns')
    response = sns.publish(
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
