#!/bin/bash

# Script for setting up django app on Amazon EC2 

echo "Starting User-Data" >> /tmp/udlog.txt

sudo yum -y install epel-release
sudo yum -y update

sudo yum -y groupinstall "Development Tools"
sudo yum -y install openssl-devel bzip2-devel libffi-devel xz-devel

# Creating folder to install dependencies
mkdir -pv /tmp/dependencies
cd /tmp/dependencies

# Downloading Python Files
sudo yum -y install wget
wget https://www.python.org/ftp/python/3.8.12/Python-3.8.12.tgz
tar xvf Python-3.8.12.tgz

# Downloading Sqlite Files
wget https://www.sqlite.org/2022/sqlite-autoconf-3390200.tar.gz
tar xvf sqlite-autoconf-3390200.tar.gz 

# Compiling Sqlite
cd sqlite-autoconf-3390200/
./configure
make
sudo make install
cd ..

# Compiling Python
cd  Python-3.8.12/
LD_RUN_PATH=/usr/local/lib  ./configure
LD_RUN_PATH=/usr/local/lib make
sudo LD_RUN_PATH=/usr/local/lib make install
cd /home/ec2-user/ # out of dependencies

# Downloading Files from s3
mkdir /home/ec2-user/buysell/
aws s3 cp s3://buysell-asif/ /home/ec2-user/buysell/ --recursive

# Installing python modules
pip3 install -r /home/ec2-user/buysell/requirements.txt

# Creating directories for gunicorn and changing ownership
sudo mkdir -p /var/{log,run}/gunicorn
sudo chown -R ec2-user:ec2-user /var/{log,run}/gunicorn

echo "User-Data Completed" >> /tmp/udlog.txt

# cd buysell/
# source .DJANGO_SECRET_KEY 
# gunicorn -c config/gunicorn/dev.py

# Logs for user data script can be found in /var/log/cloud-init-output.log