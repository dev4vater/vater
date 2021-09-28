#!/bin/bash

case "$1" in
    semaphore) sudo docker exec -it --user root semaphore /bin/sh
               exit
               ;;

            *) echo "Connects terminal to bash in container specified by argument [containerName]"
               echo "./getBash [containerName]"
               exit
               ;;
esac
