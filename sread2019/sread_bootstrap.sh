#!/bin/bash
# A few housekeeping items:

#Place authkey checker in appropriate location
#curl -o /usr/sbin/gh_authkey_checker https://files.jthan.io/binaries/gh_authkey_checker
#chmod +x /usr/sbin/gh_authkey_checker

# Append necessary lines to sshd_config and restart sshd
#echo "AuthorizedKeysCommand /usr/local/sbin/gh_authkey_checker" >> /etc/ssh/sshd_config
#echo "AuthorizedKeysCommandUser root" >> /etc/ssh/sshd_config
#systemctl restart sshd

# Add users as args to following: 
/usr/local/sbin/gh_create.py -d /Users -s /scratch/Users https://raw.githubusercontent.com/jrdemasi/scripts/master/sread2019/shortread-users.txt

# Create a cronjob to run gh_create.py every 5 minutes:
echo "*/5 * * * * root /usr/local/sbin/gh_create.py -d /Users -s /scratch/Users https://raw.githubusercontent.com/jrdemasi/scripts/master/sread2019/shortread-users.txt" > /etc/cron.d/gh_create

# CLOCK
timedatectl set-timezone America/Denver
timedatectl set-ntp on

systemctl restart crond

#Install newer version of DAStk
/opt/python/3.6.3/bin/pip3 install --upgrade DAStk
