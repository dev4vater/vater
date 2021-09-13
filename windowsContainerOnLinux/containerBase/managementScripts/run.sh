#!/bin/bash
sudo docker system prune -f
sudo docker run --privileged -it --name kvmcontainer1 --device=/dev/kvm --device=/dev/net/tun -v /sys/fs/cgroup:/sys/fs/cgroup:rw --cap-add=NET_ADMIN --cap-add=SYS_ADMIN ubuntukvm bash
