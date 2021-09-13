#!/bin/bash

sudo docker system prune -f
sudo docker volume prune -f
sudo docker network prune -f

sudo docker network create -d ipvlan \
  -o parent=enp0s8 \
  --subnet 192.168.1.0/24 \
  --ip-range 192.168.1.0/24 \
  winNet

sudo docker-compose up --build
