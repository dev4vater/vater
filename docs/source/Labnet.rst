Getting Started with Labnet
^^^^^^^^^^^^^^^^^^^^^^^^^^


.. Note:: These notes are specific to Labnet transitions but will largely apply for any network VATER is moved to

Network
~~~~~~~~

Labnet is an air gapped network used for training purposes.  Control and all required VM templates are moved onto Labnet prior to production.  Control has several internet dependencies which much be initialized prior to the move or removed once its on Labnet.  

Setup
~~~~~~

Day 0 setup instructions must be complete while Control is connected to the internet.  Setup installs all the required tools, dependencies and performs a git pull for the vater and rous repos.  The `vater restart` CLI command will build the docker containers for gitea and semaphore for the first time, which also has internet dependencies.  Once these containers are built they do not require internet connections.

Terraform
~~~~~~~~~~

The command `terraform init` is required to install new terraform modules, provider compatibility among other things.  This command must be run on control prior to Labnet transfer and must be removed from all ansible scripts once on Labnet because it has internet dependencies. 

Terraform variables are held in `rous/terraform/all.auto.tfvars`.  The top section which includes vsphere variables must be modified to fit Labnets vsphere cluster.  Change the values for vsphere credentials in `rous\terraform\variables.auto.tfvars`.  The `rootFolder` variable must be modified to match the folder on Labnets vsphere where terraform can build.  A new variable must be added `vsphere_distributed_switch` to reference the cluster's distributed switch. 

Vsphere variables for Labnet are:

::

   vsphere_server = "10.10.103.4"
   vsphere_datacenter = "lbnt-edge-dc01"
   vsphere_datastore = "cotr-mdt-ds02"
   vsphere_host = "lbnt-ops-vmh56.labnet.af.mil"
   vsphere_resource_pool = "cotr-dco"
   vsphere_distributed_switch = "cotr-edge-vdsw01"
   rootFolder = "17S"
   
::

The vsphere networks section must be modified in all `.tf` files.  When testing on ducknet, terraform builds a standard virtual switch, creates a standard port group, waits for the port group to build and then references the new network.  On Labnet there needs to be 1 data block to reference the distributed switch for the file.  

::

   data "vsphere_distributed_virtual_switch" "vds" {
     name = var.vsphere_distributed_switch
     datacenter_id = data.vsphere_datacenter.dc.id
     }

::

After this block have terraform build the distributed port groups for all required networks.  Then terraform waits 60 seconds for the port groups to build before pulling the network information from vsphere for use later when cloning the VMs. 

::
   
    resource "vsphere_distributed_port_group" "test"{
    name = "${var.class}_${var.team}_${var.testName}"
    distributed_virtual_switch_uuid = "${data.vsphere_distributed_virtual_switch.vds.id}"
    active_uplinks = ["${data.vsphere_distributed_virtual_switch.vds.uplinks[0]}",
                    "${data.vsphere_distributed_virtual_switch.vds.uplinks[1]}"
                  ]
     number_of_ports = 8
    }

    #wait time to ensure port group is built before reference
    resource "time_sleep" "wait_on_networks" {
    depends_on = [vsphere_distributed_port_group.test]
    create_duration = "60s"
   }
  
   data "vsphere_network" "test" {
   name = "${var.class}_${var.team}_test"
   datacenter_id = data.vsphere_datacenter.dc.id
   depends_on = [time_sleep.wait_on_networks]
   }

::

Ansible
~~~~~~
First you must modify vsphere credentials in `tasks/groupvars/all/creds.yml`
