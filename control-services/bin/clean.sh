#!/bin/bash

sudo rm -rf ../temp

semaphore(){
    sudo docker-compose stop semaphore semaphore_db
    sudo docker system prune -a -f
    sudo rm -rf ../data/semaphore*

}

gitea(){
    sudo docker-compose stop gitea gitea_db
    sudo docker system prune -a -f
    sudo rm -rf ../data/gitea*

}

case "$1" in
    semaphore) semaphore
               exit
               ;;
        gitea) gitea
               exit
               ;;
          all) semaphore
               gitea
               exit
               ;;
            *) echo "Cleans the data and artificats associated with a service [containerName]"
               echo "./clean [containerName]"
               exit
               ;;
esac
