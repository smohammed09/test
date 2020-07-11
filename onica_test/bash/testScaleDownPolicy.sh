#!/usr/bin/env bash

# Test ScaleUpPolicy 
region="us-east-1"
profile="default"
autoscaling_groupName="AshfaqRehman-WebApp-AutoScalingGroup-13X1JKPSXOJ73"
scaleDown_policyName="AshfaqRehman-WebApp-WebServerScaleDownPolicy-7B1XPQ4IXESQ"

aws autoscaling execute-policy --auto-scaling-group-name ${autoscaling_groupName} --policy-name ${scaleDown_policyName} --no-honor-cooldown

#autoscaling_groupID=$(aws cloudformation describe-stack-resources \
#	--profile ${profile} \
#	--region ${region} \
#	--stack-name ${webapp_stackname} \
#	--query 'StackResources[?ResourceType==`AWS::AutoScaling::AutoScalingGroup`].{PhysicalResourceId:PhysicalResourceId}' \
#	--output text
#)

#echo ${autoscaling_groupID}
#aws cloudformation update-stack \
#aws cloudformation describe-stack-resources \
#    --stack-name ${webapp_stackname}
    
