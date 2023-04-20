#!/usr/bin/env python3

import argparse

import boto3


def delete_stack(stack_name: str) -> str:
    cloudformation = boto3.client('cloudformation')
    response = cloudformation.delete_stack(
        StackName = stack_name
    )

    print(f"Deleting stack '{stack_name}' with ID {response['StackId']}...")

    return response['StackId']


def wait_for_stack_completion(stack_name: str) -> None:
    cloudformation = boto3.client('cloudformation')
    waiter = cloudformation.get_waiter('stack_delete_complete')
    try:
        waiter.wait(StackName = stack_name)
        print(f"Stack '{stack_name}' deleted successfully!")
    except Exception as exc:
        response = cloudformation.describe_stacks(StackName = stack_name)
        status = response['Stacks'][0]['StackStatus']
        raise RuntimeError(f"ERROR: Stack '{stack_name}' deletion failed with status {status}!") from exc


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Delete an AWS CloudFormation stack for a given stack name.")
    parser.add_argument('-s', '--stack_name',
                        help = "name of the stack",
                        required = True)
    args = parser.parse_args()

    delete_stack(args.stack_name)
    wait_for_stack_completion(args.stack_name)
