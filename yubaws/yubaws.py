#!/usr/bin/env python3

import argparse
import subprocess
import time
import os
from os.path import expanduser, exists
import boto3
import configparser


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["configure", "session", "otp"])
    args = parser.parse_args()
    return args


"""
Finds the name of a preconfigured MFA device
"""


def get_mfa_device():
    home = expanduser("~")
    mfa_device_file = home+"/.aws/.mfa_device"
    if not exists(mfa_device_file):
        print("You must configure an mfa device prior to using this function")
        exit(3)
    f = open(mfa_device_file, "r")
    mfa_device = f.read().strip("\n")
    f.close()
    return mfa_device


def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


""" 
Checks if a binary is in the PATH 
and returns the full path if it is 
"""


def which(program):
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def read_aws_config(file):
    config = configparser.ConfigParser()
    config.read(file)
    return config


def get_session_token():
    home = expanduser("~")
    credentials_file = home+"/.aws/credentials"
    orig_credentials_file = home+"/.aws/credentials.orig"
    if not exists(orig_credentials_file):
        print("Backing up your original credentials file")
        config = read_aws_config(credentials_file)
        with open(orig_credentials_file, 'w') as configfile:
            config.write(configfile)
    proc = subprocess.Popen(
        ['ykman', 'oath', 'accounts', 'code', get_mfa_device()], stdout=subprocess.PIPE)
    token = str(proc.communicate()[0].decode('utf-8').split()[-1])
    config = read_aws_config(credentials_file)
    orig_config = read_aws_config(orig_credentials_file)
    client = boto3.client('sts', aws_access_key_id=orig_config['default']['aws_access_key_id'],
                          aws_secret_access_key=orig_config['default']['aws_secret_access_key'])
    response = client.get_session_token(
        DurationSeconds=28800, SerialNumber=get_mfa_device(), TokenCode=token)
    config['default']['aws_access_key_id'] = response['Credentials']['AccessKeyId']
    config['default']['aws_secret_access_key'] = response['Credentials']['SecretAccessKey']
    config['default']['aws_session_token'] = response['Credentials']['SessionToken']
    with open(credentials_file, 'w') as configfile:
        config.write(configfile)
    return


"""
Used to configure a new yubikey as a virtual MFA
device for AWS. Produces an error if more than one yubikey is present
or if the yubikey doesn't support oath!
"""


def configure_new_device():
    f = filter(None, subprocess.run(
        ['ykman', 'list'], capture_output=True).stdout.decode('utf-8').split("\n"))
    keys = list(f)
    if len(keys) != 1:
        print("You must have exactly one yubikey inserted to configure a new virtual mfa device")
        exit(2)
    account_number = input("Enter your AWS account number: ")
    iam_username = input("Enter your IAM username: ")
    secret_key = input("Enter the secret key provided by AWS: ")
    oath_account_string = "arn:aws:iam::{account_number}:mfa/{iam_username}".format(
        account_number=account_number, iam_username=iam_username)
    subprocess.run(['ykman', 'oath', 'accounts', 'add',
                   '-t', oath_account_string, secret_key])
    print()
    print("We're going to generate a few OTPs now to pass back to AWS, please press your YubiKey when prompted")
    x = 0
    while x < 3:
        print()
        subprocess.run(['ykman', 'oath', 'accounts',
                       'code', oath_account_string])
        time.sleep(10)
        x = x + 1
        print()
    print("You should have at least two subsequent time based codes, go enter them in the AWS management console")
    print("To get an OTP on a one-off basis run 'ykman oath accounts code {oath_account_string}'".format(
        oath_account_string=oath_account_string))
    home = expanduser("~")
    f = open(home+"/.aws/.mfa_device", "w")
    f.write(oath_account_string)
    f.close()
    return


def get_otp():
    proc = subprocess.run(
        ['ykman', 'oath', 'accounts', 'code', get_mfa_device()])
    return


def main():
    args = parse_args()
    ykman = which('ykman')
    if ykman is None:
        print("You must have 'ykman' in your path prior to using this script")
        exit(1)
    if args.action == "configure":
        configure_new_device()
    elif args.action == "otp":
        get_otp()
    elif args.action == "session":
        get_session_token()
    return


if __name__ == '__main__':
    main()
