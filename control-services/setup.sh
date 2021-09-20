#!/bin/bash

# https://docs.gitea.io/en-us/install-with-docker/
# https://github.com/boschkundendienst/guacamole-docker-compose
# https://techblog.jeppson.org/2021/03/guacamole-docker-quick-and-easy/

# ---
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo systemctl enable docker
sudo systemctl start docker

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform

sudo apt-get update && sudo apt-get install packer

./start.sh

# --

# CentOS 7
# http://mirrors.tripadvisor.com/centos/7.9.2009/isos/x86_64/CentOS-7-x86_64-NetInstall-2009.iso

# Repo:
# http://mirror.centos.org/centos/7/os/x86_64/

# yum -y update
# systemctl enable sshd
# systemctl status sshd

