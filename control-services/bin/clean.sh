#!/bin/bash

cd ..
sudo rm -rf temp

case "$1" in
    semaphore) sudo docker-compose stop semaphore semaphore_db
               sudo docker system prune -a -f
               sudo rm -rf data/semaphore*
               exit
               ;;
        gitea) sudo docker-compose stop gitea gitea_db
               sudo docker system prune -a -f
               sudo rm -rf data/gitea*
               exit
               ;;
            *) echo "Cleans the data and artificats associated with a service [containerName]"
               echo "./clean [containerName]"
               exit
               ;;
esac
