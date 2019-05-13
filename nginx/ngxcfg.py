#!/usr/bin/env python3

"""
Assumes that nginx vhosts are managed by symlinking to files in /etc/nginx/sites-available from
/etc/nginx/sites-enabled.  Can list, enable, and disable virtual hosts in this way.

"""

import os 
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Used to enable virtual hosts within nginx')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--disable', type=str, help='disable a virtual host')
    group.add_argument('-e', '--enable', type=str, help='enable a virtual host')
    group.add_argument('-l', '--list', help='list all available sites', action="store_true")
    args = parser.parse_args()
    return(args)

def list_sites():
    """ Simply return a list of sites that are available in /etc/nginx/sites-available """
    print("A * denotes a site that is currently enabled.")
    for x in os.listdir('/etc/nginx/sites-available'):
        if x in os.listdir('/etc/nginx/sites-enabled'):
            print("{} *".format(x))
        else:
            print(x)
    return()

def disable_site(site):
    """ If site in /etc/nginx/sites-enabled, remove if symlink """
    if site in os.listdir('/etc/nginx/sites-enabled'):
        if os.path.islink(os.path.join('/etc/nginx/sites-enabled/', site)):
            os.unlink(os.path.join('/etc/nginx/sites-enabled/', site))
            print("You have to restart your webserver for these changes to take effect")
        else:
            print("Site is not a symlink, not removing!")
    else:
        print("You've entered a site that isn't currently enabled")
    return()

def enable_site(site):
    if site in os.listdir('/etc/nginx/sites-available'):
        os.symlink(os.path.join('/etc/nginx/sites-available/', site), os.path.join('/etc/nginx/sites-enabled/', site))
        print("You have to restart your webserver for these changes to take effect")
    else:
        print("You've entered a site that doesn't exist")
    return()

def main():
    args = parse_args()
    if args.list:
        list_sites()
    if args.disable:
        disable_site(args.disable)
    if args.enable:
        enable_site(args.enable)
    return()

if __name__ == '__main__':
    main()


