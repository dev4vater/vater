#!/bin/bash

# https://docs.gitea.io/en-us/install-with-docker/

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
sudo sed -i s@/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin@/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin:/usr/local/go/bin:/home/control/go/bin@g /etc/sudoers
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

if test -f /home/control/$CONFIG_REPO/.git/config; then
    echo
    echo "$CONFIG_REPO exists"
else
    git clone git@github.com:$CONFIG_USER/$CONFIG_REPO.git /home/control/$CONFIG_REPO
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


# Install dependencies for python
sudo apt-get install python3 && sudo apt-get install python3-pip
pip install -r /home/control/$SETUP_REPO/requirements/requirements.txt

### DOCKER ###
# Prompt user for environment variable values to save in .env
# Uses .env.example as the basis
echo
echo "Configuring Environment variables"
env_path="/home/control/${SETUP_REPO}/control-services/.env"
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
 done < /home/control/vater/control-services/.env.example

 echo
 echo "Saved to file"
 echo "If you wish to alter the environment variables later,"
 echo "you may change them at ${env_path}"

echo "alias vater=\"python3 ~/vater/control-services/cli/vater.py\"" > ~/.bash_aliases
source ~/.bashrc


echo
echo "ROUS configurations"
tfvars_path=/home/control/rous/terraform/variables.auto.tfvars
sem_path=/home/control/rous/tasks/group_vars/all/creds.yml
### ROUS ###
if test -f /home/control/rous/terraform/variables.tfvars.example; then
    echo -n '' > $tfvars_path
    mv /home/control/rous/tasks/group_vars/all/creds.example $sem_path

    while read tf_var; do
        if [[ $tf_var != "#"* ]] && [[ ! -z $tf_var ]]; then
            tfKey=`echo ${tf_var%=*} | cut -d' ' -f1`
            currentSemKey=''

            # find matching semaphore var
            case $tfKey in
                vsphere_user)
                    currentSemKey="vsphereUsername"
                    ;;
                vsphere_password)
                    currentSemKey="vspherePassword"
                    ;;
               *)
                   currentSemKey=""
                   ;;
            esac


            echo "Default is" $tf_var
            read -p "change? Y/N " change_tf_option < /dev/tty
            if [[ $change_tf_option == 'y' ]] || [[ $change_tf_option == 'Y' ]]; then
                # prompt for change
                read -p "${tfKey} = " tfValue < /dev/tty
                echo $tfKey = \"$tfValue\" >> $tfvars_path

                # save new value for semaphore cred
                if [[ ! -z $currentSemKey ]]; then
                    echo "change"
                    sed -i "s/$currentSemKey: .*/$currentSemKey: \"$tfValue\"/g" $sem_path
                fi
            else
                # save default var for terraform
                echo $tf_var >> $tfvars_path
            fi
        fi

    done < /home/control/rous/terraform/variables.tfvars.example
fi



# configure DoD warning banner for ssh
BANNER_DIR="/home/control/$SETUP_REPO/control-services/bin/dod_warning.txt"
sudo sed -i "s|#Banner none|Banner $BANNER_DIR|g" /etc/ssh/sshd_config


# configure static IP
netplanConfig="/etc/netplan/00-installer-config.yaml"
echo "Configuring static IP"
echo "Current configuration: "
ip address show label ens160
ip route
echo
read -p "Would you like to configure a static IP address? Y/N  " staticIPChoice
if [[ $staticIPChoice == 'Y' ]] || [[ $staticIPChoice == 'y'  ]]; then
    echo "Editing $netplanConfig"
    cat $netplanConfig | sudo tee /etc/netplan/backup >/dev/null

    while :
    do

        read -p "IPv4 address with CIDR: xxx.xxx.xxx.xxx/xx  " staticIPv4
        read -p "Gateway: xxx.xxx.xxx.xxx  " defaultGateway
        echo
         # write configuration into file
        echo "# Configured by VATER" | sudo tee $netplanConfig
        echo "network:" | sudo tee -a $netplanConfig
        echo "  version: 2" | sudo tee -a $netplanConfig
        echo "  ethernets:" | sudo tee -a $netplanConfig
        echo "    ens160:" | sudo tee -a $netplanConfig
        echo "      dhcp4: false" | sudo tee -a $netplanConfig
        echo "      addresses: [$staticIPv4]" | sudo tee -a $netplanConfig
        echo "      gateway4: $defaultGateway" | sudo tee -a $netplanConfig
        echo "      nameservers:" | sudo tee -a $netplanConfig
        echo "        addresses: [8.8.8.8, 8.8.4.4]" | sudo tee -a $netplanConfig

        # confirm configuration with user
        echo
        read -p "Would you like to save configurations? Y/N  " confirmNetplan

        if [[ $confirmNetplan == 'Y' ]] || [[ $confirmNetplan == 'y' ]]; then
            echo "saving configurations, applying netplan (network sessions like ssh will be lost)"
            sudo netplan apply
            break
        else
            echo "undoing configurations"
            cat /netplan/backup | sudo tee $netplanConfig
            read -p "Would you like to cancel configuring a static IP address? Y/N  " cancelIPConfig
            if [[ $cancelIPConfig == 'Y' ]] || [[ $cancelIPConfig == 'y' ]]; then
                break
            else
                # redo configuration of static IPv4
                continue
            fi
        fi

    done

fi

echo
echo "###### Configuration completed ######"

read -p "Would you like to reboot now? Y/N" rebootChoice
if [[ $rebootChoice == 'y' ]] || [[ $rebootChoice == 'Y' ]]; then
    echo "rebooting"
    sudo reboot
fi
