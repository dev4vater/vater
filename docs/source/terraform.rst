
Getting Started with Terraform
--------------------------------
Terraform is an infrastructure as code tool that allows the user to define virtual resources in human-readable configuration files that can be used to track infrastructure, automate changes, and standardized configurations. By implementing this resource in VATER, it will allow a consistent workflow and aid in the management of all the infrastructure.

Terraform creates and manages resources through their application programming interfaces. There are three core stages in the Terraform workflow:

- **Write**: The developer can define resources. In reference to VATER, the developer can create a configuration to deploy an application on virtual machines in the network. 
- **Plan**: Terraform creates an execution plan describing the infrastructure it will create, update, or destroy based on the current infrastructure configuration.
- **Apply**: Terraform provisions your infrastructure and updates the state file.

More Information: 

- `Terraform <https://www.terraform.io/intro>`__

How is Terraform Integrated within VATER?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: images/terraformDesign.svg

Configs
~~~~~~~
**Ansible**: Ansible is used to kick off terraform builds and provides run time variables to terraform.

**Terraform**: Terraform states is the mechanism via which it keeps track of resources that are actually deployed in the range. Project workspaces allow you to have multiple states in the same backend, tied to the same configuration. This allows you to deploy multiple distinct instances of the same infrastructure. Each student or team will have their own terraform workspace


Execution
~~~~~~~~~~

- Semaphore is a web interface for running Ansible playbooks. The playbooks define a set of hosts to configure and a list of tasks to be performed. 
- When a task is selected for execution ("Create Range"), Terraform configuration files are created using the Jinja2 template.
- A Terraform project workspace is created that will allow the deployment of multiple distinct instances of the VMs. 
- The Terraform apply while make the changes to the infrastructure resources to match the desired state (as specified by the Terraform config file).
- Once Terraform apply is run, Terraform must store the state about the managed infrastructure. This will allow Terraform to keep track of metadata, map real world resources to the configuration file, and improve performance for large infrastructure.

How to Use Terraform
~~~~~~~~~~~~~~~~~~~~

- First decide what the networks terraform will build look like. 
- Then determine what resources such as folders, VM templates ect. already exist and what resources terraform needs to build on the virtualization platform. Terraform maintains state information about the network and determines what order to build and destroy resources in.
- If there is a problem, it likely is with the virtualization platform or the VM templates not terraform. Attempt a task manually and look into errors for from the virtualization platform before spending time debugging terraform.
- Terraform resource blocks reference items that terraform will create on the virtualization platform. Data blocks reference items that already exist.
