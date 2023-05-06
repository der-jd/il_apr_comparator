#!/usr/bin/env python3

import argparse

import boto3


def _delete_stack(stack_name: str, _session: boto3.Session) -> None:
    cloudformation = _session.client('cloudformation')
    cloudformation.delete_stack(StackName = stack_name)
    print(f"Deleting stack '{stack_name}'...")


def _wait_for_stack_deletion(stack_name: str, _session: boto3.Session) -> None:
    cloudformation = _session.client('cloudformation')
    response = cloudformation.describe_stacks(StackName = stack_name)
    stack_id = response['Stacks'][0]['StackId']
    try:
        waiter = cloudformation.get_waiter('stack_delete_complete')
        waiter.wait(StackName = stack_id)
        print(f"Stack '{stack_name}' deleted successfully!")
    except Exception as exc:
        response = cloudformation.describe_stacks(StackName = stack_id)
        status = response['Stacks'][0]['StackStatus']
        raise RuntimeError(f"ERROR: Deletion of stack '{stack_name}' failed with status {status}!") from exc


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Delete an AWS CloudFormation stack for a given stack name.")
    parser.add_argument('-s', '--stack_name',
                        help = "name of the stack",
                        required = True)
    parser.add_argument('-pr', '--profile',
                        help = "name of the profile for the AWS access",
                        required = False)
    parser.add_argument('-r', '--region',
                        help = "name of the AWS region",
                        required = False)
    args = parser.parse_args()

    if args.profile and args.region:
        session = boto3.Session(profile_name = args.profile, region_name = args.region)
    elif args.profile:
        session = boto3.Session(profile_name = args.profile)
    elif args.region:
        session = boto3.Session(region_name = args.region)
    else:
        session = boto3.Session()

    _delete_stack(args.stack_name, session)
    _wait_for_stack_deletion(args.stack_name, session)
