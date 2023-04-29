#!/usr/bin/env python3

import argparse
import subprocess

import boto3


# This function should not fail on an empty changeset but instead just do nothing.
# Therefor we need to use the AWS cli here because boto3 doesn't support the "deploy" command
# in combination with the corresponding "--no-fail-on-empty-changeset" option.
def deploy_stack(template_file: str, stack_name: str, parameters: list[str], parameters_file: str) -> None:
    print(f"Deploy stack '{stack_name}'...")

    if parameters:
        parameter_option = f" --parameter-overrides {' '.join(parameters)}"
    elif parameters_file:
        parameter_option = f" --parameter-overrides file://{parameters_file}"
    else:
        parameter_option = ""

    command = ''.join([
        "aws cloudformation deploy",
        f" --template-file {template_file}",
        parameter_option,
        f" --stack-name {stack_name}",
        " --capabilities CAPABILITY_NAMED_IAM",
        " --no-fail-on-empty-changeset"])
    print(f"Run '{command}'...")
    result = subprocess.run(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE, check = False, text = True, shell = True)

    print(result.stdout, result.stderr)
    if result.returncode != 0:
        cloudformation = boto3.client('cloudformation')
        response = cloudformation.describe_stack_events(StackName = stack_name)
        raise RuntimeError(f"ERROR: Stack creation/update for '{stack_name}' failed with status '{response['StackEvents'][0]['ResourceStatus']}'!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Create or update an AWS CloudFormation stack for a given template file, " +
                                                    "a stack name and optional parameters or a parameters file.")
    parser.add_argument('-t', '--template',
                        help = "name/path of the template file",
                        required = True)
    parser.add_argument('-s', '--stack_name',
                        help = "name of the stack",
                        required = True)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p', '--parameters',
                        help = "parameters as key-value-pairs separated by space, e.g. 'key1=value1 key2=value2 ...'",
                        nargs = '*',
                        action = 'extend',
                        required = False)
    group.add_argument('-pf', '--parameters_file',
                        help = "name/path of the parameters file in JSON format for the template",
                        required = False)
    args = parser.parse_args()

    deploy_stack(args.template, args.stack_name, args.parameters, args.parameters_file)
