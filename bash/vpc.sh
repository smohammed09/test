#!/usr/bin/env bash

region="us-east-1"
profile="default"

dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#aws cloudformation update-stack \
aws cloudformation create-stack \
    --stack-name AshfaqRehman-VPC \
    --template-body file://${dir}/../cloudformation/vpc.yaml \
    --region ${region} \
    --profile ${profile} \
    --parameters \
        "ParameterKey=EnvironmentName,ParameterValue=VPC_2AZs"