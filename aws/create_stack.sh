#!/usr/bin/env bash

stack_template_file=$1
parameter_file=$2
stack_name=$3
profile=$4
region=$5

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
        --parameters file://$parameter_file \
        --stack-name $stack_name \
        --capabilities CAPABILITY_NAMED_IAM $profile_parameter $region_parameter'"

aws cloudformation create-stack \
    --template-body file://$stack_template_file \
    --parameters file://$parameter_file \
    --stack-name $stack_name \
    --capabilities CAPABILITY_NAMED_IAM $profile_parameter $region_parameter
