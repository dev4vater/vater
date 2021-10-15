#!/bin/bash

case "$1" in
    semaphore) sudo docker exec -it --user root semaphore /bin/sh
               exit
               ;;
 semaphore_db) sudo docker exec -it semaphore_db mysql -usemaphore -psemaphore
               exit
               ;;
        gitea) sudo docker exec -it gitea /bin/bash
               exit
               ;;
            *) echo "Connects terminal to bash in container specified by argument [containerName]"
               echo "./getBash [containerName]"
               exit
               ;;
esac
