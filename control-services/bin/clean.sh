#!/bin/bash

cd ..
sudo docker system prune -a -f
sudo docker-compose down --rmi all
sudo rm -rf /data
sudo rm -rf /temp
