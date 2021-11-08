#!/bin/bash

# Variables
CONFIG_REPO_NAME="rous"

restartPrep(){
    cd ..

    # Remove temp
    sudo rm -rf temp

    # Ensure folders are prepared for first time deployments
    mkdir --parents data
    mkdir --parents temp
    sudo chmod -R +x temp

    # Ensure the system is clean
    sudo docker system prune -f
}

restartSemaphore(){
    # Stop the image and force rebuilds
    sudo docker-compose stop semaphore semaphore_db
    sudo docker system prune -f

    # Rebuild images and start the containers detached from tty
    sudo docker-compose up -d --build --remove-orphans semaphore semaphore_db

    # Configure the management semaphore project
    wait-for-it localhost:4000
    wait-for-it localhost:3306
    python3 bin/setupSemaphore.py
}

restartGitea(){
    # Stop the image and force rebuilds
    sudo docker-compose stop gitea gitea_db
    sudo docker system prune -f

    # Rebuild images and start the containers detached from tty
    sudo docker-compose up -d --build --remove-orphans gitea gitea_db

    wait-for-it localhost:3000
    wait-for-it localhost:3305
    python3 bin/setupGitea.py
}

restartGuacamole(){
    # Stop the image and force rebuilds
    sudo docker-compose stop guacamole guacd guac_db
    sudo docker system prune -f

    # Grab the initial db configuration from the guacamole image to use in the guacamole_db container
    sudo sh -c  "docker run --rm guacamole/guacamole /opt/guacamole/bin/initdb.sh --postgres > ../temp/initdb.sql"

    # Rebuild images and start the containers detached from tty
    sudo docker-compose up -d --build --remove-orphans guacamole guacd guac_db
}

restartPrep

case "$1" in
    semaphore) restartSemaphore
               exit
               ;;
    guacamole) restartGuacamole
               exit
               ;;
        gitea) restartGitea
               exit
               ;;
          all) restartSemaphore
               restartGuacamole
               restartGitea
               exit
               ;;
            *) echo "Restarts a specific service and runs the setup scripts [serviceName] or all"
               echo "./restart [serviceName] or all"
               exit
               ;;
esac
