#!/bin/bash
sudo apt-get update

# Set up tools to grab docker via curl
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fSSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add 
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update

# Install docker
sudo apt install docker-ce -y

# Install docker compose

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Set docker to start on boot
sudo systemctl start docker
sudo systemctl enable docker

# Confirm virtualization is available
sudo egrep -c '(vmx|svm)' /proc/cpuinfo

# Setup internal network
echo
cat > /etc/netplan/01-netcfg.yaml <<EOF
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s8:
      addresses:
        - 192.168.1.2/24
EOF
sudo netplan apply

sudo apt-get remove -y linux-image($uname -r)
sudo apt-get install -y linux-image-5.4.0-40-generic
sudo reboot
