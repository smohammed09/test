for i in `cat bucket_list.txt`; do echo $i; `aws s3 rm s3://$i/test --recursive`; done





for i in `cat bucket_list.txt`; do echo $i; aws s3 ls s3://$i/ --recursive | sort -r; done

Hello world
