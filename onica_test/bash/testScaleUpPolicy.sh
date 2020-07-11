#!/usr/bin/env bash

# Test ScaleUpPolicy 
region="us-east-1"
profile="default"
autoscaling_groupName="AshfaqRehman-WebApp-AutoScalingGroup-13X1JKPSXOJ73"
scaleUp_policyName="AshfaqRehman-WebApp-WebServerScaleUpPolicy-6IX9W3B9J45T"

aws autoscaling execute-policy --auto-scaling-group-name ${autoscaling_groupName} --policy-name ${scaleUp_policyName} --no-honor-cooldown

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
    
