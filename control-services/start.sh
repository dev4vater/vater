
#!/bin/bash

mkdir --parents ./data
mkdir --parents ./temp
chmod -R +x ./temp
sudo docker run --rm guacamole/guacamole /opt/guacamole/bin/initdb.sh --postgres > ./temp/initdb.sql
sudo docker-compose down
sudo docker system prune -f
sudo docker-compose up -d --build --remove-orphans
sleep 10
wait-for-it localhost:8080 --strict -- rm ./temp -rf
