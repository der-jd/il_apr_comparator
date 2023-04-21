#!/usr/bin/env python3

import argparse

import boto3


def update_stack(template_file: str, stack_name: str) -> None:
    cloudformation = boto3.client('cloudformation')
    response = cloudformation.update_stack(
        TemplateBody = _parse_template(template_file),
        StackName = stack_name,
        Capabilities = [
            'CAPABILITY_NAMED_IAM',
        ]
    )
    print(f"Updating stack '{stack_name}' with ID {response['StackId']}...")


def wait_for_stack_update(stack_name: str) -> None:
    cloudformation = boto3.client('cloudformation')
    waiter = cloudformation.get_waiter('stack_update_complete')
    try:
        waiter.wait(StackName = stack_name)
        print(f"Stack '{stack_name}' updated successfully!")
    except Exception as exc:
        response = cloudformation.describe_stacks(StackName = stack_name)
        status = response['Stacks'][0]['StackStatus']
        raise RuntimeError(f"ERROR: Update of stack '{stack_name}' failed with status {status}!") from exc


def create_stack(template_file: str, stack_name: str) -> None:
    cloudformation = boto3.client('cloudformation')
    response = cloudformation.create_stack(
        TemplateBody = _parse_template(template_file),
        StackName = stack_name,
        Capabilities = [
            'CAPABILITY_NAMED_IAM',
        ]
    )
    print(f"Creating stack '{stack_name}' with ID {response['StackId']}...")


def _parse_template(template_file: str) -> str:
    with open(template_file, encoding = 'utf-8') as file:
        template_body = file.read()
    boto3.client('cloudformation').validate_template(TemplateBody = template_body)
    return template_body


def wait_for_stack_creation(stack_name: str) -> None:
    cloudformation = boto3.client('cloudformation')
    waiter = cloudformation.get_waiter('stack_create_complete')
    try:
        waiter.wait(StackName = stack_name)
        print(f"Stack '{stack_name}' created successfully!")
    except Exception as exc:
        response = cloudformation.describe_stacks(StackName = stack_name)
        status = response['Stacks'][0]['StackStatus']
        raise RuntimeError(f"ERROR: Creation of stack '{stack_name}' failed with status {status}!") from exc


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Create an AWS CloudFormation stack for a given template file and a stack name.")
    parser.add_argument('-t', '--template',
                        help = "name/path of the template file",
                        required = True)
    parser.add_argument('-s', '--stack_name',
                        help = "name of the stack",
                        required = True)
    args = parser.parse_args()

    if stack_exists(args.stack_name):
        update_stack(args.template, args.stack_name)
    else:
        create_stack(args.template, args.stack_name)
        wait_for_stack_creation(args.stack_name)

