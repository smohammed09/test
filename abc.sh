for i in `cat bucket_list.txt`; do echo $i; `aws s3 rm s3://$i/test --recursive`; done

for i in `cat bucket_list.txt`; do echo $i; aws s3 ls s3://$i/ --recursive | sort -r; done


=======
Hello world

Hello world 2

Hello world 3

Hello world 4

Script excluding builds on jenkins KEEP_BACKUP_DAYS

#!/bin/bash

echo "Syncing backup folder to $JENKINS_BACKUP_BUCKET"
KEEP_BACKUP_DAYS=7
DATE=`date '+%Y-%m-%d_%H-%M'`
ARCHIVE_NAME="BASIC-"$DATE
#sed -e "s/<useSecurity>true<\/useSecurity>/<useSecurity>false<\/useSecurity>/g" $JENKINS_HOME/config.xml > $JENKINS_HOME/config-file-for-test-jenkins-cluster.xml
tar -czf ${ARCHIVE_NAME}.tar.gz --exclude='workspace' --exclude='caches' --exclude='jobs/**/builds/*/*' --exclude='war' --warning=no-file-changed -C $JENKINS_HOME .
#tar -czf archive_without_jobs.tar.gz --exclude='workspace' --exclude='caches' --exclude='jobs' --warning=no-file-changed -C $JENKINS_HOME .
aws s3 cp ${ARCHIVE_NAME}.tar.gz s3://$JENKINS_BACKUP_BUCKET --sse --only-show-errors
#aws s3 cp archive_without_jobs.tar.gz s3://$JENKINS_BACKUP_BUCKET --sse --only-show-errors
echo
find "`pwd`" -type f -mtime +$KEEP_BACKUP_DAYS -name 'FULL*.tar.gz' -delete

Including backup

#!/bin/bash

echo "Syncing backup folder to $JENKINS_BACKUP_BUCKET"
KEEP_BACKUP_DAYS=7
DATE=`date '+%Y-%m-%d_%H-%M'`
ARCHIVE_NAME="FULL-"$DATE
#sed -e "s/<useSecurity>true<\/useSecurity>/<useSecurity>false<\/useSecurity>/g" $JENKINS_HOME/config.xml > $JENKINS_HOME/config-file-for-test-jenkins-cluster.xml
tar -czf ${ARCHIVE_NAME}.tar.gz --exclude='workspace' --exclude='caches' --warning=no-file-changed -C $JENKINS_HOME .
#tar -czf archive_without_jobs.tar.gz --exclude='workspace' --exclude='caches' --exclude='jobs' --warning=no-file-changed -C $JENKINS_HOME .
aws s3 cp ${ARCHIVE_NAME}.tar.gz s3://$JENKINS_BACKUP_BUCKET --sse --only-show-errors
#aws s3 cp archive_without_jobs.tar.gz s3://$JENKINS_BACKUP_BUCKET --sse --only-show-errors
echo
find "`pwd`" -type f -mtime +$KEEP_BACKUP_DAYS -name 'FULL*.tar.gz' -delete

security compliance backup jobs

#!/bin/bash

echo "Syncing backup folder to $JENKINS_BACKUP_BUCKET"
KEEP_BACKUP_DAYS=7
DATE=`date '+%Y-%m-%d_%H-%M'`
ARCHIVE_NAME="CONFIG-"$DATE
sed -e "s/<useSecurity>true<\/useSecurity>/<useSecurity>false<\/useSecurity>/g" $JENKINS_HOME/config.xml > $JENKINS_HOME/config-file-for-test-jenkins-cluster.xml
tar -czf ${ARCHIVE_NAME}.tar.gz --exclude='workspace' --exclude='caches' --exclude='plugins' --exclude='jobs/**/builds/*/*' --exclude='war' --warning=no-file-changed -C $JENKINS_HOME .
#tar -czf ${ARCHIVE_NAME}.tar.gz --warning=no-file-changed -C $JENKINS_HOME .
aws s3 cp ${ARCHIVE_NAME}.tar.gz s3://$JENKINS_BACKUP_BUCKET --sse --only-show-errors
echo
find "`pwd`" -type f -mtime +$KEEP_BACKUP_DAYS -name 'FULL*.tar.gz' -delete
>>>>>>> 2be152bd658f0fa69e4257db9b2aafbf0d596194
