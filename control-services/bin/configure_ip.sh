#!/bin/bash

set -e

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