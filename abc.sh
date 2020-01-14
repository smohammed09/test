for i in `cat bucket_list.txt`; do echo $i; `aws s3 rm s3://$i/test --recursive`; done

for i in `cat bucket_list.txt`; do echo $i; aws s3 ls s3://$i/ --recursive | sort -r; done

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::277983268692:user/root"
            },
            "Action": "execute-api:Invoke",
            "Resource": "arn:aws:execute-api:us-east-1:953067469207:1fct0iklz0/v1/GET/pets"
        }
    ]
}
