#!/bin/bash

set -e

sudo apt-get update -y
sudo apt-get upgrade -y

# Install go for building semaphore
sudo rm -rf /usr/local/go

# check machine type for arm support
machineType=$(uname -m)
if [[ $machineType == "x86_64" ]] || [[ $machineType == "amd64" ]]; then
    wget https://go.dev/dl/go1.17.7.linux-amd64.tar.gz -P /tmp/
    sudo tar -C /usr/local/ -xzf /tmp/go1.17.7.linux-amd64.tar.gz
    rm -f /tmp/go1.17.7.linux-amd64.tar.gz
elif [[ $machineType == "aarch64" ]] || [[ $machineType == "arm64" ]]; then
    echo "WARNING: limited support for arm, press any key if you understand"
    read -n 1 -s
    wget https://go.dev/dl/go1.17.7.linux-arm64.tar.gz -P /tmp/
    sudo tar -C /usr/local/ -xzf /tmp/go1.17.7.linux-arm64.tar.gz
    rm -f /tmp/go1.17.7.linux-arm64.tar.gz
fi

echo "export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin" | sudo tee -a /etc/profile
sudo sed -i s@/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin@/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin:/usr/local/go/bin:$HOME/go/bin@g /etc/sudoers
source /etc/profile

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
if [[ $machineType == "x86_64" ]] || [[ $machineType == "amd64" ]];then
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
elif [[ $machineType == "aarch64" ]]|| [[ $machineType == "arm64" ]]; then
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.6.1/docker-compose-linux-aarch64" -o /usr/local/bin/docker-compose
fi
sudo chmod +x /usr/local/bin/docker-compose

# Point to hashicorp repo and install terraform and packer
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository -y "deb [arch=$(dpkg --print-architecture)] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install -y packer

if [[ $machineType == "x86_64" ]] || [[ $machineType == "amd64" ]]; then
    sudo apt-get update && sudo apt-get install -y terraform
elif [[ $machineType == "aarch64" ]]|| [[ $machineType == "arm64" ]]; then
    wget https://releases.hashicorp.com/terraform/1.2.5/terraform_1.2.5_linux_arm64.zip -P /tmp/
    sudo apt install -y unzip
    sudo unzip /tmp/terraform_1.2.5_linux_arm64.zip -d /usr/local/
    echo "export PATH=$PATH:/usr/local/terraform:$HOME/terraform" | sudo tee -a /etc/profile
    sudo sed -i s@/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin:/usr/local/go/bin:$HOME/go/bin@/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin:/usr/local/go/bin:$HOME/go/bin:/usr/local/terraform@g /etc/sudoers
    source /etc/profile
fi

# Install a tool used in start script
sudo apt-get install -y wait-for-it

# Install nginx
sudo apt-get install nginx
sudo systemctl enable nginx
sudo systemctl start nginx

# Clean up
sudo apt autoremove -y