#!/usr/bin/env python36

"""
A script that takes at least one GitHub username as an argument, creates a unix user 
of the same name, sets a default (insecure) password, and pulls the users SSH keys from GH.
Tested on CentOS7.  Known insecure because of os and also because setting hard-coded passwords.
This is to be used for AWS and other temporary, non-security-intensive resources.
"""


import subprocess
import sys
import os

x = 0
while x < len(sys.argv):
    if x == 0:
        x = x + 1
        pass
    else:
        print("Creating user {}".format(sys.argv[x]))
        subprocess.check_output(["useradd", "-m", sys.argv[x]])
        print("Creating ssh directory...")
        subprocess.check_output(["mkdir", "--mode=700", "/home/{}/.ssh".format(sys.argv[x])])
        print("Adding keys for user {}".format(sys.argv[x]))
        subprocess.check_output(["curl", "-o", "/home/{}/.ssh/authorized_keys".format(sys.argv[x]), "https://github.com/{}.keys".format(sys.argv[x])])
        print("Fixing permissions on keys...")
        subprocess.check_output(["chown", "-R", "{0}:{0}".format(sys.argv[x]), "/home/{}/.ssh".format(sys.argv[x])])
        subprocess.check_output(["chmod", "644", "/home/{}/.ssh/authorized_keys".format(sys.argv[x])])
        print("Setting a default password...")
        os.system("echo {}:asdfasdf | chpasswd".format(sys.argv[x]))
        x = x + 1

