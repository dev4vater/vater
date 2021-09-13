#!/bin/bash

sudo docker system prune -f
sudo docker volume prune -f
sudo docker network prune -f

# sudo docker network create -d macvlan -o parent=enp0s8 \
#  --subnet 192.168.1.0/24 \
#  --gateway 192.168.1.2 \
#  --ip-range 192.168.1.0/24 \
#  devNet

sudo docker-compose up --build
