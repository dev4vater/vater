# dev

## Tasks

- [x] Set up Container Host VM from ISO (Ubuntu 20.04.1)
- [x] Install docker and docker-compose
- [x] Set up git repository on Container Host VM
- [x] Set up Kali VM from OVA (Kali Linux 2021.2)
- [x] Configure Virtualbox networking
- [ ] Build initial docker-compose setup
- [ ] Create script to set up Container Host VM network
- [ ] Build VyOS docker container with this [demo](https://github.com/vyos/vyos-build/tree/current/docker-vyos)
- [ ] Pursue concurrent os-family containers with this [demo](https://medium.com/axon-technologies/installing-a-windows-virtual-machine-in-a-linux-docker-container-c78e4c3f9ba1)
- [x] Complete first pass proof of concept diagram

## Parking lot

- [ ] Should the development environment emulate the Kali VM connecting to infrastructure available via VPN?
- [ ] Install wireguard on Kali?

## Endstate

![Map](https://github.com/uwardlaw/dev/blob/main/diagrams/modelA.png)

## Development Environment

![Map](https://github.com/uwardlaw/dev/blob/main/diagrams/proofOfConcept.drawio.png)

### Specifications

* Host
  * Virtualbox Version 6.1.22 r144080 (Qt5.6.2)
  * Windows 10 Home Version 10.0.19043 Build 19043
* Guests
  * ContainerHost configuration
    * [Ubuntu 20.04.1-live-server-amd64 ISO (Focal Fossa)](http://old-releases.ubuntu.com/releases/20.04.1/ubuntu-20.04.1-live-server-amd64.iso)
    * General (Basic) - Type: Linux
    * General (Basic) - Version: Ubuntu (64-bit)
    * System (MotherBoard) - Base Memory: 4096 MB
    * System (Processor) - Processors: 2
    * System (Processor) - Enable Nested VT-x/AMD0V: Enabled
    * Storage - Normal (VDI) 70.00 GB, dynamically allocated 
    * Network (Adapter 1) - Attached to: NAT
    * Network (Adapter 2) - Attached to: Internal Network (intnet)
  * Kali
    * [Kali Linux 2021.2-virtualbox-amd64 OVA](https://images.kali.org/virtual-images/kali-linux-2021.2-virtualbox-amd64.ova)
* Services
  * docker-ce (5:20.10.8~3-0~ubuntu-focal)
  * containerd.io (1.4.9-1)
  * docker-ce-cli (5:20.10.8~3-0~ubuntu-focal)
  * docker-compose (1.29.2, build 5becea4c)

### Files

`dev@dev:~/dev$ tree .`
```
.
├── README.md
├── setupUbuntuFirstTime.sh           # Script to perform initial containerHost setup 
├── twoMetasploitableContainers       # Proof of concept for two metasploitable containers on one host 
│   ├── clean.sh                      # Script to stops and remove containers and docker network
│   ├── docker-compose.yml            # Instructions to build two metasploitable containers
│   ├── ms2
│   │   ├── Dockerfile                # Instructions to build one metasploitable container
│   │   └── entrypoint.sh             # Script to run inside the container after it starts
│   └── start.sh                      # Script to clean dangling docker objects and execute docker-compose.yml
└── windowsContainerOnLinux           # Proof of concept for a windows container on a Linux system
    ├── clean.sh                       
    ├── docker-compose.yml
    ├── start.sh
    └── win
        ├── Dockerfile
        └── entrypoint.sh
```
### Diagrams

<details>
 <summary></summary>
</details>

### containerHost VM (Ubuntu 20.04.1) Configuration Post Install

1. Optional: You may choose to work through PuTTy via SSH rather than the hypervisor manager (Virtualbox). PuTTy provides host to guest copy and paste, text appearance configuration, and does not have the Virtualbox cursor capture behavior
    * When installing the Ubuntu ISO for the Container Host VM, either choose to install OpenSSH during the installation process or install it with `apt-get` later
    * In Virtualbox configure a port forwarding rule for the Container Host VM (Host port 2222 -> guest port 22). The host port can be any valid service port not currently in use on the host machine
    * SSH from PuTTy to localhost:2222 

2. Initial Ubuntu repo update

```shell
sudo apt-get update
sudo apt-get upgrade
```

3. [Install Docker Engine](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

```shell
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
    
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo systemctl enable docker
sudo systemctl start docker
sudo docker run hello-world
```

4. Confirm test results

```
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.
```

5. [Install Docker Compose](https://docs.docker.com/compose/install/) (Linux tab)

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

6. Confirm test results

```
# Build will probably vary
docker-compose version 1.29.2, build 5becea4c
```

7. Optionally [Install command-line compleition](https://docs.docker.com/compose/completion/)

```
sudo curl \
    -L https://raw.githubusercontent.com/docker/compose/1.29.2/contrib/completion/bash/docker-compose \
    -o /etc/bash_completion.d/docker-compose
source ~/.bashrc
```

8. Internal Network Configuration

Create the netplan
`sudo nano /etc/netplan/99_config.yaml`
```
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s8:
      addresses:
        - 192.168.1.2/24
```
`sudo netplan apply`

9. Grab vyos-build repo to make routers

```
sudo git clone https://github.com/vyos/vyos-build.git
```

### Kali VM Configuration

Currently none. Plug and play unless you want to connect via SSH with PuTTy.

## Configure Networking

Need to place the Kali box on the internal network, with that 192.168.1.1/24 address listed in the diagram. [Kali network configuration](https://kali.training/topic/configuring-the-network/). [Ifupdown tutorial](https://techpiezo.com/linux/switch-back-to-ifupdown-etc-network-interfaces-in-ubuntu/)

Edit `/etc/network/interfaces`

```
source /etc/network/interfaces.d/*
# The loopback network interface
auto lo
iface lo inet loopback

auto eth1
iface eth1 inet static
address 192.168.1.1
netmask 255.255.255.0
```

Execute `sudo systemctl restart networking`

Set SSH to start automatically.

```
sudo systemctl enable ssh.service
sudo systemctl start ssh.service
``` 

### Virtualbox Networking Configuration

## Resources
* https://docs.docker.com/compose/networking/
* https://docs.docker.com/engine/faq/
* https://docs.docker.com/network/network-tutorial-macvlan/
* https://docs.docker.com/compose/compose-file/compose-file-v2/#networks
* https://www.aquasec.com/cloud-native-academy/docker-container/docker-networking/
* https://callistaenterprise.se/blogg/teknik/2017/12/28/multi-platform-docker-images/
* https://medium.com/axon-technologies/installing-a-windows-virtual-machine-in-a-linux-docker-container-c78e4c3f9ba1
