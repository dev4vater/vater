#!/bin/bash

# Clean up dangling items
sudo docker system prune -f

# If they're running, shutdown the previous containers
sudo docker container rm dev2_ms2_1 dev2_ms2_1 -f

# Remove and then re-create the network
# See https://gist.github.com/nerdalert/28168b016112b7c13040#ipvlan-l3-mode-example-usage
sudo docker network rm ms2Net
sudo docker network create -d ipvlan \
  -o parent=enp0s8 \
  --subnet 192.168.1.0/24 \
  --ip-range 192.168.1.0/24 \
  ms2Net

# Build and then run the containers in the background
sudo docker-compose up --build -d
