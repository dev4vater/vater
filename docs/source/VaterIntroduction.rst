.. image:: images/MADDUCK.jpg

Theory of VATER
===============

VATER should be a server that hosts containerized services for the automated management of virtual ranges. In a production environment, taking a content repo as a exact IAC description of the desired training environment, VATER provides the ability to build and destroy individual vms, individual networks (students), and groups of networks (classes) as well as interact granularly with the environment.

VATER consists of:

- Ubuntu Server 20.04 with 2 vCPUs, 4 GB RAM, and 60 GB storage in /
- docker (version)
- Semaphore (version)
- Semaphore_db
- Gitea (verson)
- Gitea_db
- Jenkins (version)
- vater cli: written in python utilizing argparse
