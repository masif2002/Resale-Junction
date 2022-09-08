#!/bin/bash

# Script for setting up django application on Ubuntu Server (Non-AWS)

# Installing Docker
sudo apt-get update 
sudo apt-get install  \
   ca-certificates \
   curl \
   gnupg \
   lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg 
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin 

# Installing AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip
unzip awscliv2.zip
sudo ./aws/install

# Configuring AWS Credentials
export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
export AWS_DEFAULT_REGION=us-east-1

# Pulling Django Artefacts
mkdir -p ~/home/asif/buysell
aws s3 cp s3://buysell-asif/ /home/asif/buysell/ --recursive

# Installing dependencies
sudo apt-get install build-essential checkinstall
sudo apt install libssl-dev libncurses5-dev libsqlite3-dev libreadline-dev libtk8.6 libgdm-dev libdb4o-cil-dev libpcap-dev -y
cd /opt
sudo wget https://www.python.org/ftp/python/3.8.12/Python-3.8.12.tgz
sudo tar xzf Python-3.8.12.tgz
cd Python-3.8.12
sudo ./configure --enable-optimizations
sudo make install

sudo apt install python3-pip 
pip3.8 install -r /home/asif/buysell/requirements.txt
sudo mkdir -p /var/{log,run}/gunicorn
sudo chown -cR $USER:$USER /var/{log,run}/gunicorn

# Configuring Nginx
sudo apt install nginx 
sudo systemctl start nginx

sudo mkdir -p /etc/nginx/sites-available/
sudo mkdir -p /etc/nginx/sites-enabled/
sudo cp /home/asif/buysell/mysite/nginx/techin48 /etc/nginx/sites-available/techin48
sudo ln -s /etc/nginx/sites-available/techin48 /etc/nginx/sites-enabled/techin48
sudo systemctl restart nginx

# Serving Static Files
sudo mkdir -pv /var/www/asif.techin48.com/static/
sudo chown -cR $USER:$USER /var/www/asif.techin48.com/
cd /home/asif/buysell
python3.8 manage.py collectstatic 
sudo systemctl restart nginx

# SSL Certifictes with Lets Encrypt
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
sudo certbot --nginx # Prompt Opens