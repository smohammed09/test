FROM jenkins/jenkins:lts

USER root
RUN apt-get update && apt-get install -y gosu python-pip rsync curl software-properties-common
RUN apt-get update && apt-get install -y openssh-client
RUN pip install awscli