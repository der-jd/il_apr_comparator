#!/usr/bin/env python3

import argparse
import subprocess

import boto3


# This function should not fail on an empty changeset but instead just do nothing.
# Therefor we need to use the AWS cli here because boto3 doesn't support the "deploy" command
# in combination with the corresponding "--no-fail-on-empty-changeset" option.
def _deploy_stack(_args: argparse.Namespace) -> None:
    print(f"Deploy stack '{_args.stack_name}'...")

    command = ''.join([
        "aws cloudformation deploy",
        f" --template-file {_args.template}",
        _get_parameter_argument(_args.parameters, _args.parameter_file),
        f" --stack-name {_args.stack_name}",
        " --capabilities CAPABILITY_NAMED_IAM",
        " --no-fail-on-empty-changeset",
        _get_profile(_args.profile),
        _get_region_argument(_args.region)])

    print(f"Run '{command}'...")
    result = subprocess.run(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE, check = False, text = True, shell = True)

    print(result.stdout, result.stderr)
    if result.returncode != 0:
        cloudformation = boto3.client('cloudformation')
        response = cloudformation.describe_stack_events(StackName = _args.stack_name)
        raise RuntimeError(f"ERROR: Stack creation/update for '{_args.stack_name}' failed with status '{response['StackEvents'][0]['ResourceStatus']}'!")


def _get_parameter_argument(parameters: list[str], parameter_file: str) -> str:
    if parameters:
        parameter_argument = f" --parameter-overrides {' '.join(parameters)}"
    elif parameter_file:
        parameter_argument = f" --parameter-overrides file://{parameter_file}"
    else:
        parameter_argument = ""
    return parameter_argument


def _get_profile(profile: str) -> str:
    if profile:
        profile_argument = f" --profile {profile}"
    else:
        profile_argument = ""
    return profile_argument


def _get_region_argument(region: str) -> str:
    if region:
        region_argument = f" --region {region}"
    else:
        region_argument = ""
    return region_argument


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Create or update an AWS CloudFormation stack for a given template file, " +
                                                    "a stack name and optional parameters or a parameter file.")
    parser.add_argument('-t', '--template',
                        help = "name/path of the template file",
                        required = True)
    parser.add_argument('-s', '--stack_name',
                        help = "name of the stack",
                        required = True)
    parser.add_argument('-pr', '--profile',
                        help = "name of the profile for AWS CLI",
                        required = False)
    parser.add_argument('-r', '--region',
                        help = "name of the AWS region",
                        required = False)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p', '--parameters',
                        help = "parameters as key-value-pairs separated by space, e.g. 'key1=value1 key2=value2 ...'",
                        nargs = '*',
                        action = 'extend',
                        required = False)
    group.add_argument('-pf', '--parameter_file',
                        help = "name/path of the parameter file in JSON format for the template",
                        required = False)
    args = parser.parse_args()

    _deploy_stack(args)
