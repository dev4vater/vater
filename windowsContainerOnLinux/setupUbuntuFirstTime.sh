#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Run with sudo"
  exit
fi

apt-get update

# Set up tools to grab docker via curl
apt-get install -y      \
    apt-transport-https \
    ca-certificates     \
    curl                \
    gnupg-agent         \
    software-properties-common
curl \
    -fSSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add
apt-key fingerprint 0EBFCD88
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt update

# Install docker
apt install docker-ce -y

# Install docker compose
curl \
    -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Install command-line compleition
curl \
    -L https://raw.githubusercontent.com/docker/compose/1.29.2/contrib/completion/bash/docker-compose \
    -o /etc/bash_completion.d/docker-compose
source ~/.bashrc

# Set docker to start on boot
systemctl enable docker

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

exit
# Downgrade the kernel to 5.4.0-40
sudo apt-get remove -y linux-image-$(uname -r)
sudo apt-get install -y linux-image-5.4.0-40-generic
sudo reboot
