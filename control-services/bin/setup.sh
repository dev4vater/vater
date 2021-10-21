#!/bin/bash

# https://docs.gitea.io/en-us/install-with-docker/
# https://github.com/boschkundendienst/guacamole-docker-compose
# https://techblog.jeppson.org/2021/03/guacamole-docker-quick-and-easy/

# ---

# https://docs.github.com/en/developers/overview/managing-deploy-keys#deploy-keys
# Generate an SSH key with prompt and print out the public key
SETUP_REPO="shoe-rack"
CONFIG_REPO="rous"
ORG_OR_USER="uwardlaw"
SSH_PATH="/home/control/.ssh"
SETUP_SSH_KEY_PATH="$SSH_PATH/$SETUP_REPO"
CONFIG_SSH_KEY_PATH="$SSH_PATH/$CONFIG_REPO"

sudo apt-get update -y
sudo apt-get upgrade -y

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

# Key creation for key deployment and git setup

echo "Checking for key at $SETUP_SSH_KEY_PATH"
if test -f "$SETUP_SSH_KEY_PATH"; then
    echo "Key exists"
else
    echo "Key does not exist"
    ssh-keygen -b 2048 -t rsa -f ~/.ssh/$SETUP_REPO -q -N ""
fi
cat $SETUP_SSH_KEY_PATH.pub

echo
echo "Copy this key to the $SETUP_REPO repo as a deploy key. Press any key when done."

read -n 1 -s

echo "Checking for key at $CONFIG_SSH_KEY_PATH"
if test -f "$CONFIG_SSH_KEY_PATH"; then
    echo "Key exists"
else
    echo "Key does not exist"
    ssh-keygen -b 2048 -t rsa -f ~/.ssh/$CONFIG_REPO -q -N ""
fi
cat $CONFIG_SSH_KEY_PATH.pub

echo
echo "Copy this key to the ROUS $CONFIG_REPO as a deploy key. Press any key when done."

read -n 1 -s

# Setup SSH config file

cat <<EOF >$SSH_PATH/config
Host $SETUP_REPO
  Hostname ssh.github.com
  Port 443
  IdentityFile $SETUP_SSH_KEY_PATH

Host $CONFIG_REPO
  Hostname ssh.github.com
  Port 443
  IdentityFile $CONFIG_SSH_KEY_PATH
EOF

# Pull the git repos

git clone git@github.com:$ORG_OR_USER/$SETUP_REPO.git
git clone git@github.com:$ORG_OR_USER/$CONFIG_REPO.git

# Setup the URLs

git remote set-url origin "ssh://git@$SETUP_REPO/$ORG_OR_USER/$SETUP_REPO.git
git remote set-url origin "ssh://git@$CONFIG_REPO/$ORG_OR_USER/$CONFIG_REPO.git



./restart.sh
