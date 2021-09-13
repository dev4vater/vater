#!/bin/bash

# If they're running, shutdown the previous containers
sudo docker container rm twometasploitablecontainers_ms2-1_1 twometasploitablecontainers_ms2-2_1 -f

# Remove network
sudo docker network rm ms2Net
