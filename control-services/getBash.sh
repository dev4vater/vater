#!/bin/bash

case "$1" in
    semaphore) sudo docker exec -it --user root semaphore /bin/sh
               exit
               ;;

            *) echo "./getBash [containerName]"
               exit
               ;;
esac
