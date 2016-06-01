#VERSION 1.0
FROM ubuntu:14.04
MAINTAINER Hemant Kumar, hemakuma@cisco.com
RUN apt-get update && apt-get -y upgrade && apt-get install -y  vim git python curl openssh-server supervisor zsh  python-pip python-dev build-essential
#nxtoolkit install
WORKDIR /opt
RUN git clone https://github.com/datacenter/nxtoolkit
WORKDIR nxtoolkit
RUN python setup.py install