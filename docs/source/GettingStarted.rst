Downloading VM server
=====================

-  Manually provision a control VM using Ubuntu 20.04 Server
-  https://releases.ubuntu.com/20.04/
-  2 vCPUS
-  4 GB RAM
-  60 GB storage in / 

.. Important:: The user and hostname need to be Control or you need to edit the config.json


VATER Repository Information
============================
-  Clone VATER repository to your home directory(~)

   -  In your home directory(~) run:
   -  ``git clone https://github.com/dev4vater/vater``

-  Execute setup.sh  

   - Manually run: 
   - ``~/vater/control-services/bin/setup.sh``
   - setup.sh will create a RSA key pair if one does not exist and print the public key to the terminal

  
-  To run VATER:

   - Manually copy the public RSA key
   - Manually input public RSA key into ``marissaeinhorn/rous`` as a deploy key
   - setup.sh will pull marissaeinhorn/rous locally
   - Manually run ``vater restart``
  
