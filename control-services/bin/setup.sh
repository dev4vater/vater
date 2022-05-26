#!/bin/bash

# https://docs.gitea.io/en-us/install-with-docker/
# https://github.com/boschkundendienst/guacamole-docker-compose
# https://techblog.jeppson.org/2021/03/guacamole-docker-quick-and-easy/

# ---

# https://docs.github.com/en/developers/overview/managing-deploy-keys#deploy-keys
# Generate an SSH key with prompt and print out the public key
set -e

SETUP_REPO="vater"
CONFIG_REPO="rous"
SETUP_USER="dev4vater"
CONFIG_USER="marissaeinhorn"
SSH_PATH="/home/control/.ssh"
SETUP_SSH_KEY_PATH="$SSH_PATH/$SETUP_REPO"
CONFIG_SSH_KEY_PATH="$SSH_PATH/$CONFIG_REPO"
SEMAPHORE_SSH_KEY_PATH="$SSH_PATH/semaphore"
SSH_AUTH_KEYS_PATH="/home/control/.ssh/authorized_keys"

sudo apt-get update -y
sudo apt-get upgrade -y

# Install go for building semaphore
sudo rm -rf /usr/local/go
wget https://go.dev/dl/go1.17.7.linux-amd64.tar.gz -P /tmp/
sudo tar -C /usr/local/ -xzf /tmp/go1.17.7.linux-amd64.tar.gz
rm -f /tmp/go1.17.7.linux-amd64.tar.gz

echo "export PATH=$PATH:/usr/local/go/bin:/home/control/go/bin" | sudo tee -a /etc/profile
source /etc/profile

# Check go version
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
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
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
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install -y terraform
sudo apt-get update && sudo apt-get install -y packer

# Install a tool used in start script
sudo apt-get install -y wait-for-it

# Clean up
sudo apt autoremove -y

# Create .ssh if it doesn't exist
mkdir -p $SSH_PATH

# Key creation for the Semaphore container
#   used to execute commands like Terraform

echo "Checking for key at $SEMAPHORE_SSH_KEY_PATH"
if test -f "$SEMAPHORE_SSH_KEY_PATH"; then
    echo
    echo "Key exists"
else
    echo
    echo "Key does not exist"
    ssh-keygen -b 2048 -t rsa -f $SEMAPHORE_SSH_KEY_PATH -q -N ""
fi

# Create authorized keys with only the Semaphore key
sudo cat $SEMAPHORE_SSH_KEY_PATH.pub > $SSH_AUTH_KEYS_PATH
sudo chmod 600 $SSH_AUTH_KEYS_PATH

# Key creation for key deployment and git setup
eval `ssh-agent -s`

echo "Checking for key at $SETUP_SSH_KEY_PATH"
if test -f "$SETUP_SSH_KEY_PATH"; then
    echo
    echo "Key exists"
else
    echo
    echo "Key does not exist"
    ssh-keygen -b 2048 -t rsa -f $SETUP_SSH_KEY_PATH -q -N ""
fi

echo
cat $SETUP_SSH_KEY_PATH.pub

echo
ssh-keygen -l -f $SETUP_SSH_KEY_PATH

echo
ssh-add $SETUP_SSH_KEY_PATH

echo
echo "Copy this key to github as an SSH key, call it $SETUP_REPO deploy. Press any key when done."

read -n 1 -s

echo "Checking for key at $CONFIG_SSH_KEY_PATH"
if test -f "$CONFIG_SSH_KEY_PATH"; then
    echo
    echo "Key exists"
else
    echo
    echo "Key does not exist"
    ssh-keygen -b 2048 -t rsa -f $CONFIG_SSH_KEY_PATH -q -N ""
fi

echo
cat $CONFIG_SSH_KEY_PATH.pub

echo
ssh-keygen -l -f $CONFIG_SSH_KEY_PATH

echo
ssh-add $CONFIG_SSH_KEY_PATH

echo
echo "Copy this key to github as an SSH key, call it $CONFIG_REPO deploy. Press any key when done."

read -n 1 -s

# Setup SSH config file

cat <<EOF >$SSH_PATH/config
Host github.com
  Hostname ssh.github.com
  Port 443
  IdentityFile $CONFIG_SSH_KEY_PATH
  StrictHostKeyChecking no
EOF

# Pull the config repo first, if it does not exist

if test -f /home/control/$CONFIG_REPO/.git/config; then
    echo
    echo "$CONFIG_REPO exists"
else
    git clone git@github.com:$CONFIG_REPO/$CONFIG_REPO.git /home/control/$CONFIG_REPO
fi

# Set up for using SSH keys moving forward with 2 repos

cat <<EOF >$SSH_PATH/config
Host $SETUP_REPO
  HostName ssh.github.com
  User git
  Port 443
  IdentityFile $SETUP_SSH_KEY_PATH
  IdentitiesOnly yes

Host $CONFIG_REPO
  HostName ssh.github.com
  User git
  Port 443
  IdentityFile $CONFIG_SSH_KEY_PATH
  IdentitiesOnly yes
EOF

# Setup the URLs
echo
echo "Change origin urls for $SETUP_REPO and $CONFIG_REPO"
git --git-dir /home/control/$SETUP_REPO/.git remote set-url origin "git@$SETUP_REPO:$SETUP_USER/$SETUP_REPO.git"
git --git-dir /home/control/$CONFIG_REPO/.git remote set-url origin "git@$CONFIG_REPO:$CONFIG_USER/$CONFIG_REPO.git"

# Git pull from origin main (master branch of repo on github)
# validate local repo is up to date
echo
echo "Confirm $SETUP_REPO is up to date"
git --git-dir /home/control/$SETUP_REPO/.git pull origin main
echo
echo "Confirm $CONFIG_REPO is up to date"
git --git-dir /home/control/$CONFIG_REPO/.git pull origin main

echo "alias vater=\"python3 ~/vater/control-services/cli/vater.py\"" > ~/.bash_aliases
source ~/.bashrc

# configure DoD warning banner for ssh
BANNER_DIR="/home/control/$SETUP_REPO/control-services/bin/dod_warning.txt"
sudo sed -i "s|#Banner none|Banner $BANNER_DIR|g" /etc/ssh/sshd_config


echo "rebooting"
sudo reboot
