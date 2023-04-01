#!/usr/bin/env bash

stack_template_file=$1
stack_name=$2
profile=$3
region=$4

if [ -z $profile ]; then
    profile_parameter=""
else
    profile_parameter="--profile $profile"
fi

if [ -z $region ]; then
    region_parameter=""
else
    region_parameter="--region $profile"
fi

echo "Run 'aws cloudformation create-stack \
        --template-body file://$stack_template_file \
        --stack-name $stack_name \
        --capabilities CAPABILITY_NAMED_IAM $profile_parameter $region_parameter'"

aws cloudformation create-stack \
    --template-body file://$stack_template_file \
    --stack-name $stack_name \
    --capabilities CAPABILITY_NAMED_IAM $profile_parameter $region_parameter
