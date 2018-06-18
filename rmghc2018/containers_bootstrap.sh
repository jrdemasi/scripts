#!/bin/bash

USERS="jrdemasi hynesgra timmonsd"

# You need not modify below this line



# A few housekeeping items:
timedatectl set-timezone America/Denver

# Requirements for our useradd script
yum install -y epel-release
yum install -y python36 python36-devel

curl -o /var/tmp/gh_create.py https://raw.githubusercontent.com/jrdemasi/scripts/master/gh_create.py
chmod +x /var/tmp/gh_create.py

# Add users as args to following: 
/var/tmp/gh_create.py https://raw.githubusercontent.com/jrdemasi/scripts/master/rmghc2018/nascent-users.txt

# Create a cronjob to run gh_create.py every 5 minutes:
echo "*/5 * * * * root /var/tmp/gh_create.py https://raw.githubusercontent.com/jrdemasi/scripts/master/rmghc2018/nascent-users.txt" > /etc/cron.d/gh_create
