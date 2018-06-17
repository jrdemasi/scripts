#!/bin/bash

yum install -y epel-release
yum install -y python36

curl -o /var//tmp/gh_create.py https://raw.githubusercontent.com/jrdemasi/scripts/master/gh_create.py
chmod +x /var//tmp/gh_create.py

# Add users as args to following: 
/var/tmp/gh_create.py 

# Create a cronjob to run gh_create.py every 5 or 10 minutes:

# Install bioconda, modify system env: 

