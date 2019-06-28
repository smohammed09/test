{
    "Version": "2008-10-17",
    "Id": "Policy1357935677554",
    "Statement": [
        {
            "Sid": "Stmt1357935647218",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::368057246517:role/shah-lambda-role-datahub-testing"
            },
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::shah-testing-datahub2"
        },
        {
            "Sid": "Stmt1357935676138",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::368057246517:role/shah-lambda-role-datahub-testing"
            },
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::shah-testing-datahub2/*"
        }
    ]
}
