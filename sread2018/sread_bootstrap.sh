#!/bin/bash
# A few housekeeping items:
curl -o /var/tmp/gh_create.py https://raw.githubusercontent.com/jrdemasi/scripts/master/sread2018/gh_create.py
chmod +x /var/tmp/gh_create.py

# Add users as args to following: 
/var/tmp/gh_create.py -d /Users -s /scratch/Users https://raw.githubusercontent.com/jrdemasi/scripts/master/sread2018/shortread-users.txt

# Create a cronjob to run gh_create.py every 5 minutes:
echo "*/5 * * * * root /var/tmp/gh_create.py -d /Users -s /scratch/Users https://raw.githubusercontent.com/jrdemasi/scripts/master/sread2018/shortread-users.txt" > /etc/cron.d/gh_create

# CLOCK
timedatectl set-timezone America/Denver
timedatectl set-ntp on

systemctl restart crond

#add picard after the fact
yum -y localinstall /scratch/admin/for_jon/biof-picard2_6_0-2.6.0-1.x86_64.rpm
