#!/bin/bash

# Ensure folders are prepared for first time deployments
mkdir --parents ../data
mkdir --parents ../temp
chmod -R +x ../temp

# Grab the initial db configuration from the guacamole image to use in the guacamole_db container
sudo docker run --rm guacamole/guacamole /opt/guacamole/bin/initdb.sh --postgres > ../temp/initdb.sql

# Ensure the system is clean
sudo docker-compose down
sudo docker system prune -f

# Rebuild images and start the containers detached from tty
sudo docker-compose up -d --build --remove-orphans

# Preempt some known race conditions between databases and their apps
sleep 10
rm -r ../temp

# Configure the management semaphore project

python3 ./setupSemaphore.py

# Configure gitea with mirrored ROUS repo

sudo docker exec -it gitea su git bash -c "gitea admin user create --admin --username config --password config --email a@a.a"

python3 ./setupGitea.py

sudo docker exec -it gitea su git bash -c "gitea admin user delete --username config"
