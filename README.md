# dev

## Tasks

- [x] Set up Container Host VM from ISO (Ubuntu 20.04.1)
- [x] Install docker and docker-compose
- [x] Set up git repository on Container Host VM
- [x] Set up Kali VM from OVA (Kali Linux 2021.2)
- [x] Configure Virtualbox networking
- [x] Build initial docker-compose setup
- [x] Create script to set up Container Host VM network
- [ ] Build VyOS docker container with this [demo](https://github.com/vyos/vyos-build/tree/current/docker-vyos)
- [x] Pursue concurrent os-family containers with this [demo](https://medium.com/axon-technologies/installing-a-windows-virtual-machine-in-a-linux-docker-container-c78e4c3f9ba1)
- [x] Complete first pass proof of concept diagram
- [x] Confirm exploitation of one service in metasploitable container does not affect the other
- [ ] Confirm that crashing a service in one metasploitable container does not affect the other

## Parking lot

- [ ] Should the development environment emulate the Kali VM connecting to infrastructure available via VPN?
- [ ] Install wireguard on Kali?
- [ ] Rewrite the iptables rules for windows machine

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
 <summary>Range Model A</summary>
 ![Map](https://github.com/uwardlaw/dev/blob/main/diagrams/modelA.png)
</details>

### containerHost VM (Ubuntu 20.04.1) Configuration

1. Create a new virtual machine with the same resources as above and load the Ubuntu ISO. The new virtual machine wizard prompts for OS type, version, memory, and storage, but the processor, nested VT-x, and network must be configured from the VM settings after the wizard closes.

2. Optional: You may choose to work through PuTTy via SSH rather than the hypervisor manager (Virtualbox). PuTTy provides host to guest copy and paste, text appearance    configuration, and does not have the Virtualbox cursor capture behavior
    - When installing the Ubuntu ISO for the Container Host VM, either choose to install OpenSSH during the installation process or install it with `apt-get` later
    - In Virtualbox configure a port forwarding rule for the Container Host VM (Host port 2222 -> guest port 22). The host port can be any valid service port not currently in use on the host machine
    - SSH from PuTTy to localhost:2222 

3. Follow the guided OS installation from the live booted Ubuntu

   - Setup whatever user / server name you want. I use `dev` for all options
   - During drive partitioning I expanded the `ubuntu-lv` device (mounted at `/`) to maximum allowed size. This simplified the file structure later
   - I opt to install the `OpenSSH Server` during install, so I can reboot and SSH in via PuTTy 

3. Clone this repo

   ```sh
   dev@dev:~$ git clone https://github.com/uwardlaw/dev/
   ```

4. Run the setup script

   ```sh
   dev@dev:~$ ./dev/setupUbuntuFirstTime.sh
   ```
   Select `<No>` at the `Removing linux-image` prompt

5. Run post install tests

   Confirm device mounted at `/` has ~70G 
   ```
   dev@dev:~/dev$ lsblk
   NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
   loop0                       7:0    0   55M  1 loop /snap/core18/1880
   loop1                       7:1    0 71.3M  1 loop /snap/lxd/16099
   loop2                       7:2    0 29.9M  1 loop /snap/snapd/8542
   sda                         8:0    0   70G  0 disk
   ├─sda1                      8:1    0    1M  0 part
   ├─sda2                      8:2    0    1G  0 part /boot
   └─sda3                      8:3    0   69G  0 part
     └─ubuntu--vg-ubuntu--lv 253:0    0   69G  0 lvm  /
   sr0                        11:0    1 1024M  0 rom
   ```
   
   Confirm response >0
   ```
   dev@dev:~/dev$ egrep -c '(vmx|svm)' /proc/cpuinfo
   2
   ```

   Confirm Kernel version is 5.4.0-40
   ```
   dev@dev:~/dev$ uname -r
   5.4.0-40-generic
   ```

   Confirm hello-world runs
   ```
   dev@dev:~/dev$ sudo docker run hello-world

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

   Confirm docker-compose returns a version, build will may vary
   ```
   dev@dev:~/dev$ docker-compose --version`
   docker-compose version 1.29.2, build 5becea4c
   ```

   Confirm adapter came up with `192.168.1.2` configured 
   ```
   dev@dev:~/dev$ ip a
   1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
       link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
       inet 127.0.0.1/8 scope host lo
          valid_lft forever preferred_lft forever
       inet6 ::1/128 scope host
          valid_lft forever preferred_lft forever
   2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
       link/ether 08:00:27:1f:60:5b brd ff:ff:ff:ff:ff:ff
       inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic enp0s3
          valid_lft 86398sec preferred_lft 86398sec
       inet6 fe80::a00:27ff:fe1f:605b/64 scope link
          valid_lft forever preferred_lft forever
   3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
       link/ether 08:00:27:7d:61:40 brd ff:ff:ff:ff:ff:ff
       inet 192.168.1.2/24 brd 192.168.1.255 scope global enp0s8
          valid_lft forever preferred_lft forever
       inet6 fe80::a00:27ff:fe7d:6140/64 scope link
          valid_lft forever preferred_lft forever
   4: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default
       link/ether 02:42:88:ea:b2:d5 brd ff:ff:ff:ff:ff:ff
       inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
          valid_lft forever preferred_lft forever
   ```

### Kali VM Configuration

Place the Kali box on the internal network, with the 192.168.1.1/24 address listed in the diagram. [Kali network configuration](https://kali.training/topic/configuring-the-network/). [Ifupdown tutorial](https://techpiezo.com/linux/switch-back-to-ifupdown-etc-network-interfaces-in-ubuntu/)

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
