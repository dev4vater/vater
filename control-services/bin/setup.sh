#!/bin/bash

# https://docs.gitea.io/en-us/install-with-docker/

# ---

# https://docs.github.com/en/developers/overview/managing-deploy-keys#deploy-keys
# Generate an SSH key with prompt and print out the public key
set -e
# directory of setup.sh
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"


# Install required packages
echo "Installing required packages"
source ${__dir}/install_requirements.sh

# Configure ssh for github
echo "Configuring ssh for github repos"
source ${__dir}/configure_git.sh


# configure DoD warning banner for ssh
BANNER_DIR="$HOME/$SETUP_REPO/control-services/bin/dod_warning.txt"
sudo sed -i "s|#Banner none|Banner $BANNER_DIR|g" /etc/ssh/sshd_config

# configure static IP
source ${__dir}/configure_ip.sh

echo
echo "###### Configuration completed ######"

read -p "Would you like to reboot now? Y/N " rebootChoice
if [[ $rebootChoice == 'y' ]] || [[ $rebootChoice == 'Y' ]]; then
    echo "rebooting"
    sudo reboot
fi
