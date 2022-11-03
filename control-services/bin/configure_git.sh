#!/bin/bash

set -e

SETUP_REPO="vater"
CONFIG_REPO="rous"
SETUP_USER="dev4vater"
CONFIG_USER="dev4vater"
SSH_PATH="$HOME/.ssh"
SETUP_SSH_KEY_PATH="$SSH_PATH/$SETUP_REPO"
CONFIG_SSH_KEY_PATH="$SSH_PATH/$CONFIG_REPO"
SEMAPHORE_SSH_KEY_PATH="$SSH_PATH/semaphore"
SSH_AUTH_KEYS_PATH="$HOME/.ssh/authorized_keys"

tput reset
echo "Is the following setup repo correct? (username/repo)"
echo "$SETUP_USER/$SETUP_REPO"
read -p 'Y/N ? ' changeOption < /dev/tty
if [[ $changeOption == "N" ]] || [[ $changeOption == "n" ]]; then
   read -p "Enter setup username: " SETUP_USER < /dev/tty
   read -p "Enter setup repo: " SETUP_REPO < /dev/tty
fi

echo "Is the following config repo correct? (username/repo)"
echo "$CONFIG_USER/$CONFIG_REPO"
read -p 'Y/N ? ' changeOption < /dev/tty
if [[ $changeOption == "N" ]] || [[ $changeOption == "n" ]]; then
   read -p "Enter setup username: " CONFIG_USER < /dev/tty
   read -p "Enter setup repo: " CONFIG_REPO < /dev/tty
fi

# Create .ssh if it doesn't exist
mkdir -p $SSH_PATH

# Setting up git global configurations
echo "Setting up git configurations"
read -p 'github username: ' gitUsername
read -p 'github email: ' gitEmail
git config --global user.name "$gitUsername"
git config --global user.email "$gitEmail"

# Key creation for the Semaphore container
#   used to execute commands like Terraform

echo "Checking for key at $SEMAPHORE_SSH_KEY_PATH"
if test -f "$SEMAPHORE_SSH_KEY_PATH"; then
    echo
    echo "Key exists"
    SEMVAR="$(cat $SSH_PATH/semaphore.pub)"
    if [[ $(grep -c "$SEMVAR" $SSH_PATH/authorized_keys) -lt 1 ]]; then
        echo "key is authorized"
        cat $SSH_PATH/semaphore.pub >> $SSH_PATH/authorized_keys
    fi
else
    echo
    echo "Key does not exist"
    ssh-keygen -b 2048 -t rsa -f $SEMAPHORE_SSH_KEY_PATH -q -N ""
    cat $SSH_PATH/semaphore.pub >> $SSH_PATH/authorized_keys
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
echo "Copy this key to your github settings as an SSH key, call it $SETUP_REPO deploy. Press any key when done."

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
echo "Copy this key to your github settings as an SSH key, call it $CONFIG_REPO deploy. Press any key when done."

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

if test -f $HOME/$CONFIG_REPO/.git/config; then
    echo
    echo "$CONFIG_REPO exists"
else
    git clone git@github.com:$CONFIG_USER/$CONFIG_REPO.git $HOME/$CONFIG_REPO
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
echo "Change origin urls for $SETUP_REPO and $CONFIG_REPO"
git --git-dir $HOME/$SETUP_REPO/.git remote set-url origin "git@$SETUP_REPO:$SETUP_USER/$SETUP_REPO.git"
git --git-dir $HOME/$CONFIG_REPO/.git remote set-url origin "git@$CONFIG_REPO:$CONFIG_USER/$CONFIG_REPO.git"

# Git pull from origin main (master branch of repo on github)
# validate local repo is up to date
echo
echo "Confirm $SETUP_REPO is up to date"
git --git-dir $HOME/$SETUP_REPO/.git pull origin main
echo
echo "Confirm $CONFIG_REPO is up to date"
git --git-dir $HOME/$CONFIG_REPO/.git pull origin main


# Install dependencies for python
sudo apt-get install -y python3 && sudo apt-get install -y python3-pip
pip install -r $HOME/$SETUP_REPO/requirements/requirements.txt

### DOCKER ###
# Prompt user for environment variable values to save in .env
# Uses .env.example as the basis
tput reset
echo "Configuring Environment variables"
env_path="$HOME/${SETUP_REPO}/control-services/.env"
touch $env_path
echo "# .env created " `date` > $env_path
while read line_str; do
    if [[ $line_str != "#"* ]] && [[ ! -z $line_str ]]; then
        echo "Default is" $line_str
        read -p 'Change? Y/N '  changeOption < /dev/tty
        if [[ -z $changeOption ]] || [[ $changeOption == "N" ]] || [[ $changeOption == "n" ]]; then
            # writeout default to .env
            echo $line_str >> $env_path
        else
            # prompt user and save into file
            envKey=${line_str%=*}
            read -p "${envKey}=" envValue < /dev/tty
            echo "${envKey}=${envValue}" >> $env_path
        fi
    fi
 done < $HOME/$SETUP_REPO/control-services/.env.example

 echo
 echo "Saved to file"
 echo "If you wish to alter the environment variables later,"
 echo "you may change them at ${env_path}"

# export environment vars for vater/control-services/config.py
echo "export SETUP_USER=$SETUP_USER" >> $HOME/.bashrc
echo "export SETUP_REPO=$SETUP_REPO" >> $HOME/.bashrc
echo "export CONFIG_USER=$CONFIG_USER" >> $HOME/.bashrc
echo "export CONFIG_REPO=$CONFIG_REPO" >> $HOME/.bashrc
echo "export HOSTNAME=$(hostname)" >> $HOME/.bashrc

echo "alias vater=\"python3 $HOME/$SETUP_REPO/control-services/cli/vater.py\"" > $HOME/.bash_aliases
source $HOME/.bashrc


tput reset
echo "ROUS configurations"
tfvars_path=$HOME/$CONFIG_REPO/terraform/variables.auto.tfvars
### ROUS ###
if test -f $HOME/$CONFIG_REPO/terraform/variables.tfvars.example; then
    echo -n '' > $tfvars_path

    while read tf_var; do
        if [[ $tf_var != "#"* ]] && [[ ! -z $tf_var ]]; then
            tfKey=`echo ${tf_var%=*} | cut -d' ' -f1`

            echo "Default is" $tf_var
            read -p "change? Y/N " change_tf_option < /dev/tty
            if [[ $change_tf_option == 'y' ]] || [[ $change_tf_option == 'Y' ]]; then
                # prompt for change
                read -p "${tfKey} = " tfValue < /dev/tty
                echo $tfKey = \"$tfValue\" >> $tfvars_path

            else
                # save default var for terraform
                echo $tf_var >> $tfvars_path
            fi
        fi

    done < $HOME/$CONFIG_REPO/terraform/variables.tfvars.example
fi
