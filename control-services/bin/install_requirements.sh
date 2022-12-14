#!/bin/bash

set -e

sudo apt-get update -y
sudo apt-get upgrade -y

# Install go for building semaphore
sudo rm -rf /usr/local/go
wget https://go.dev/dl/go1.19.3.linux-amd64.tar.gz -P /tmp/
sudo tar -C /usr/local/ -xzf /tmp/go1.19.3.linux-amd64.tar.gz
sudo rm -f /tmp/go1.19.3.linux-amd64.tar.gz

# Fix pathing to use go installed binaries
export PATH=$PATH:$HOME/go/bin:/usr/local/go/bin
# add to /etc/profile for persistence if it's not there already
if [[ $(grep export /etc/profile) == *"/home/control/go/bin:/usr/local/go/bin"* ]]; then
    echo "path to go binaries exists in /etc/profile"
else
    sudo cp /etc/profile /etc/profile.backup
    echo "export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin" | sudo tee -a /etc/profile
    sudo sed -i "s%/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin%/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin:/home/control/go/bin:/usr/local/go/bin%g" /etc/sudoers 
fi

# Confirm go was installed and exported
go version

# Install npm
sudo apt install -y npm

# Install docker
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \

sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg --batch --yes
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get -y update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
sudo systemctl enable docker
sudo systemctl start docker

# Install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Point to hashicorp repo and install terraform and packer
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository -y "deb [arch=$(dpkg --print-architecture)] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install -y packer

sudo apt-get update && sudo apt-get install -y terraform

# Install a tool used in start script
sudo apt-get install -y wait-for-it

# Install nginx
sudo apt-get install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx

# Clean up
sudo apt autoremove -y
