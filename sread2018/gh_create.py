#!/usr/bin/env python3.6

"""
A version of gh_create that expects to run on a cfn cluster.
Checks if script is running on login/master node before
doing things like creating scratch and homedirs
"""

import argparse
import crypt
import grp
import os
import pwd
import shutil
import subprocess
from urllib.parse import urlparse
from urllib.request import urlopen


class UserMgr(object):
    def __init__(self, user, homedir, password):
        self.users = [u.strip() for u in user]
        self.homedir = homedir
        self.password = password
        self.sshkeys = {}
        self.passhashes = {}
        # A shared group for all users to be added to (in addition to "private"
        # username-based group)
        self.shared_grp = 'workshop'

    def get_keys(self):
        for u in self.users:
            try:
                with urlopen('https://github.com/{0}.keys'.format(u)) as url:
                    keydata = url.read().decode('utf-8')
            except Exception as e:
                print('{0}: Warning: {1}'.format(u, e))
                keydata = ''
            self.sshkeys[u] = keydata
        return()

    def get_hashes(self):
        for u in self.users:
            _salt = crypt.mksalt(method = crypt.METHOD_SHA512)
            self.passhashes[u] = crypt.crypt(self.password, _salt)
        return()

    def mkusers(self):
        subprocess.run(['/sbin/groupadd',
                        '--force',  # Exit on success if exists
                        self.shared_grp])
        for u in self.users:
            subprocess.run(['/usr/sbin/useradd',
                            '--create-home',
                            '--home-dir', self.homedir,
                            '--groups', self.shared_grp,
                            '--shell', '/bin/bash',
                            u])
        return()

    def prep_ssh(self):
        for u in self.users:
            # Could also use pwd.getpwnam(u).pw_dir instead of
            # os.path.expanduser(...)
            _sshdir = os.path.join(os.path.expanduser('~{0}'.format(u)),
                                   '.ssh')
            _sshfile = os.path.join(_sshdir, 'authorized_keys')
            _uid = pwd.getpwnam(u).pw_uid
            _gid = grp.getgrnam(u).gr_gid
            os.makedirs(_sshdir,
                        exist_ok = True)
            os.chmod(_sshdir, 0o700)
            os.chown(_sshdir, _uid, _gid)
            with open(_sshfile, 'w') as f:
                f.write(self.sshkeys[u])
            os.chmod(_sshfile, 0o600)
            os.chown(_sshfile, _uid, _gid)
        return()

    def mod_hashes(self):
        # Mimic usermod/passwd/etc. behaviour.
        shutil.copy2('/etc/shadow', '/etc/shadow-')
        with open('/etc/shadow', 'r') as f:
            _shadow = f.readlines()
        for idx, line in enumerate(_shadow[:]):
            _line = line.split(':')
            _uname = _line[0]
            if _uname in self.users:
                _line[1] = self.passhashes[_uname]
            _shadow[idx] = ':'.join(_line)
        with open('/etc/shadow', 'w') as f:
            f.write(''.join(_shadow))
        return()

    def main(self):
        self.get_keys()
        self.get_hashes()
        self.mkusers()
        self.prep_ssh()
        self.mod_hashes()
        return()

def chk_URL(in_str):
    is_url = False
    _url = urlparse(in_str[0])
    if _url.scheme in ('http', 'https'):
        is_url = True
    if not is_url:
        return(in_str)
    else:
        with urlopen(in_str[0]) as url:
            users = [i.strip() for i in url.read().decode('utf-8').split()]
        return(users)

def parseArgs():
    args = argparse.ArgumentParser(description = ('Prep a user'))
    args.add_argument('-h', '--homedir',
                      dest = 'homedir',
                      default = '/home',
                      help = ('The default base for homedirs.'
                              'Default: /home'))

    args.add_argument('-p', '--password',
                      dest = 'password',
                      default = 'asdfasdf',
                      help = ('The password to use for the user(s). '
                              'Default: asdfasdf'))
    args.add_argument('user',
                      nargs = '+',
                      help = ('The username(s) to add; must match GitHub '
                              'username(s). Can be a space-separated list OR '
                              'a URL to a file containing a space-separated '
                              'list (single-line; must begin with http:// or '
                              'https://)'))
    return(args)

def main():
    args = vars(parseArgs().parse_args())
    args['user'] = chk_URL(args['user'])
    um = UserMgr(**args)
    um.main()
    return()

if __name__ == '__main__':
    main()
