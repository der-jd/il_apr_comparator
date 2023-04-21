#!/usr/bin/env python3

import argparse
import os
import subprocess

import boto3


# This function should not fail on an empty changeset but instead just do nothing.
# Therefor we need to use the AWS cli here because boto3 doesn't support the "deploy" command
# in combination with the corresponding "--no-fail-on-empty-changeset" option.
def deploy_stack(template_file: str, stack_name: str) -> None:
    print(f"Deploy stack '{stack_name}'...")
    template_file = os.path.abspath(template_file)
    command = f"aws cloudformation deploy --template-file {template_file} --stack-name {stack_name} --capabilities CAPABILITY_NAMED_IAM --no-fail-on-empty-changeset"
    result = subprocess.run(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE, check = False, text = True)
    print(result.stdout, result.stderr)
    if result.returncode != 0:
        cloudformation = boto3.client('cloudformation')
        response = cloudformation.describe_stack_events(StackName = stack_name)
        raise RuntimeError(f"ERROR: Stack creation/update for '{stack_name}' failed with status '{response['StackEvents'][0]['ResourceStatus']}'!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Create or update an AWS CloudFormation stack for a given template file and a stack name.")
    parser.add_argument('-t', '--template',
                        help = "name/path of the template file",
                        required = True)
    parser.add_argument('-s', '--stack_name',
                        help = "name of the stack",
                        required = True)
    args = parser.parse_args()

    deploy_stack(args.template, args.stack_name)
