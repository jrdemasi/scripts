#!/bin/bash

yum install -y epel-release
yum install -y python36

curl -o /tmp/gh_create.py https://raw.githubusercontent.com/jrdemasi/scripts/master/gh_create.py
chmod +x /tmp/gh_create.py

# Add users as args to following: 
/tmp/gh_create.py 

# Install bioconda, modify system env: 

# Cleanup: 
rm -rf /tmp/gh_create.py
