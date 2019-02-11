#!/bin/bash

# This script takes a CentOS 7 minimal install and performs common operations
# that happen across most of my installs, including disabled selinux.  If you
# don't want to disable selinux, then don't run this script as-is.

set -e

TIMEZONE="America/Denver"
IPV6=false # set to true if you want to install shorewall6

# Sorry, but we're turning off selinux.
# If you're some stranger reading this, do not pawn your opinions off on me
# or rage that I'm turning selinux off. This is my life.
sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config

# Let's get rid of this junk
systemctl disable NetworkManager
systemctl disable firewalld
systemctl enable network

# Install epel
echo "Installing epel"
yum install -y epel-release

# Need real firewall plz
echo "Installing shorewall"
yum install -y shorewall
if [[ ${IPV6} == "true" ]]
  then
    echo "Installing shorewall6"
    yum install -y shorewall6
fi


# Please install vim
echo "Installing vim and making it look nice"
yum install -y vim
echo "colorscheme desert" >> ~/.vimrc

# Set time
echo "Setting the timezone to ${TIMEZONE} and enabling ntp"
yum install -y ntp
timedatectl set-timezone ${TIMEZONE}
timedatectl set-ntp on

# Update everything, then reboot
echo "Updating everything that's left!"
yum update -y

for i in {10..1};
  do echo "Rebooting in ${i}...";
  sleep 1;
done
reboot
