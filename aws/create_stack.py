#!/usr/bin/env python3

import argparse

import boto3


def create_stack(template_file: str, stack_name: str) -> str:
    cloudformation = boto3.client('cloudformation')
    response = cloudformation.create_stack(
        TemplateURL = template_file,
        StackName = stack_name,
        Capabilities=[
            'CAPABILITY_NAMED_IAM',
        ]
    )

    print(f"Created stack '{stack_name}' with ID {response['StackId']}")

    return response['StackId']

def wait_for_stack_completion(stack_name: str) -> None:
    cloudformation = boto3.client('cloudformation')
    waiter = cloudformation.get_waiter('stack_create_complete')
    try:
        waiter.wait(StackName = stack_name)
        print(f"Stack '{stack_name}' created successfully!")
    except:
        response = cloudformation.describe_stacks(StackName = stack_name)
        status = response['Stacks'][0]['StackStatus']
        raise RuntimeError(f"ERROR: Stack {stack_name} creation failed with status {status}!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Create an AWS CloudFormation stack for a given template file and a stack name.")
    parser.add_argument('-t', '--template',
                        help = "name/path of the template file",
                        required = True)
    parser.add_argument('-s', '--stack_name',
                        metavar = '--stack-name',
                        help = "name of the stack",
                        required = True)
    args = parser.parse_args()

    create_stack(args.template, args.stack_name)
    wait_for_stack_completion(args.stack_name)
