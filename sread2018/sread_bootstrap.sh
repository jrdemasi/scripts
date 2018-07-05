#!/bin/bash
# A few housekeeping items:
curl -o /var/tmp/gh_create.py https://raw.githubusercontent.com/jrdemasi/scripts/master/sread2018/gh_create.py
chmod +x /var/tmp/gh_create.py

# Add users as args to following: 
/var/tmp/gh_create.py -d /Users -s /scratch/Users https://raw.githubusercontent.com/jrdemasi/scripts/master/sread2018/shortread-users.txt

# Create a cronjob to run gh_create.py every 5 minutes:
echo "*/5 * * * * root /var/tmp/gh_create.py -d /Users -s /scratch/Users https://raw.githubusercontent.com/jrdemasi/scripts/master/sread2018/shortread-users.txt" > /etc/cron.d/gh_create

