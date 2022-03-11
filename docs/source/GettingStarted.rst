VirtualBox/VMware Set Up
========================

Vater will be run on a VM server. VirutalBox or VMWare will work for
this project, although experience has seen VirtualBox creating fewer
issues. - Virtual Box Set Up - VMWare Set Up

Downloading VM server
=====================

-  Manually provision a control VM using Ubuntu 20.04 Server
-  https://releases.ubuntu.com/20.04/
-  User and Hostname must equal Control

   -  2 vCPUS
   -  4 GB RAM
   -  60 GB storage in / # Set up

-  Clone Vater repository to your home directory(~)

   -  In you home directory(~) run “git clone
      https://github.com/uwardlaw/vater”

-  Navigate to setup.sh

   -  cd vater/control-services/bin

-  Run set up script

   -  ./setup.sh # Info about rous

-  uwardlaw/rous is a config_repo that is a private repo that configures
   what platform to build the range on
-  For current SNIT use, you will be unable to access the uwardlaw/rous
   to copy the RSA key and thus you will not be able to set up new
   ranges, but you can still set up vater on your control VM
-  The below steps should be done if you have access to the rous repo:

   -  setup.sh will create a RSA key pair if one does not exist and
      print the public key to the terminal
   -  Manually copy the public RSA key
   -  Manually input public RSA key into uwardlaw/rous as a deploy key #
      Running vater

-  Once setup.sh is complete
-  To run Vater:

   -  cd vater/control-services
   -  sudo docker-compose up

-  This will set up and run the docker containing Vater and Vater will
   start

   -  NOTE: Currently (March 2022) There is an issue with the env name
      on the semaphore configuration that causes a build fail

-  Ctrl-C to exit Vater
