#!/bin/bash

# Repo for netinstall
# http://mirror.centos.org/centos/7/os/x86_64/

yum -y update
systemctl enable sshd
systemctl status sshd
tar -zxvf ansible-automation-platform-setup-bundle-1.2.1-1.tar.gz
cp ./inventory ./ansible-automation-platform-setup-bundle-1.2.1-1/inventory 
./ansible-automation-platform-setup-bundle-1.2.1-1/setup.sh
