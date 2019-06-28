#!/bin/bash

file="datalake-s3-replication.zip"
lambda_name="datalake-s3-replication"
artifact_bucket_name="datalake-artifacts"
branch="$(git rev-parse --abbrev-ref HEAD)"

rm -r dist
mkdir dist

zip -g dist/$file source/**/*.py source/resource/*

echo
echo
echo -n "You are deploying a new lambda version. Is this for release or testing [r/t] :"
read output

current_date=`date +%Y-%m-%d`

if [ $output == "r" ]; then
	if [ $branch != "master" ]; then 
		echo -n "This is not the master branch, are you sure? type 'yes']:"
		read  confirm
		if  [ -z $confirm ] || [ $confirm != "yes" ]; then
			echo "You did not answer yes. Exiting..."
			exit 
		fi
	fi
	echo "archiving to $artifact_bucket_name/lambdas/$lambda_name/$current_date/$file"
	aws s3api put-object --bucket $artifact_bucket_name --key lambdas/$lambda_name/$current_date/$file --body dist/$file
	result=$?
	if [ $result == 0 ]; then
	    echo -e "Archived $file successfully\n"
	else
	    echo -e "Archiving $file failed. Check if the file exists\n"
	fi
	echo "deploying to $artifact_bucket_name/lambdas/$file"
	aws s3api put-object --bucket $artifact_bucket_name --key lambdas/$file --body dist/$file
    result=$?
	if [ $result == 0 ]; then
	    echo "You can use this URL to deploy lambda: https://s3.amazonaws.com/$artifact_bucket_name/lambdas/$file"
	fi
elif [ $output == "t" ]; then
	echo -n "Would you like a subfolder under the test folder? [leave blank for no]:"
	read  subfolder
	
	if [ -z $subfolder ]; then
		testfolder="test"
	else
		testfolder="test/$subfolder"
	fi
	echo "deploying to $artifact_bucket_name/lambdas/$lambda_name/$testfolder/$file"
	aws s3api put-object --bucket $artifact_bucket_name --key lambdas/$lambda_name/$testfolder/$file --body dist/$file
    result=$?
	if [ $result == 0 ]; then
	    echo "You can use this URL to deploy lambda: https://s3.amazonaws.com/$artifact_bucket_name/lambdas/$lambda_name/$testfolder/$file"
	fi
else 
	echo "Please enter type r or t"
fi 