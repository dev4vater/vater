Getting Started with Ansible
=======

Basic Terminology:

- **Control node**: the host on which you use Ansible to execute tasks on the managed nodes

- **Managed node**: a host that is configured by the control node

- **Host inventory**: a list of managed nodes. By default, Ansible represents the machines it manages in a file (INI, YAML, and so on) that puts all of your managed machines in groups of your own choosing.

- **Playbook**: a set of repeatable tasks for more complex configurations .A playbook contains one or more plays which define a set of hosts to configure and a list of tasks to be performed.

- **Module**: code that performs a particular common task such as adding a user, installing a package, etc. Ansible works by connecting to your nodes and pushing out scripts called “Ansible modules” to them. Most modules accept parameters that describe the desired state of the system. Ansible then executes these modules and removes them when finished.

A basic command in Ansible will accomplish: 

- Selecting machines to execute against from inventory. In the context of VATER, the developer will select a group of Virtual Machines (VMs) they wish to execute the command against. 

- Connects to those machines (or network devices, or other managed nodes).

- Copies one or more modules to the remote machines and starts execution there. 

More Information on Getting Started with Ansible: 
- `Getting Started <https://docs.ansible.com/ansible/latest/user_guide/intro_getting_started.html#intro-getting-started>`
- `User Guide <https://docs.ansible.com/ansible/latest/user_guide/index.html>`
 
Ansible & VMware
=======
Ansible provides various modules to manage VMware infrastructure. In the context of VATER, Ansible will allow management of the range VMs. 

The best way to interact with your hosts is to use the VMware dynamic inventory plugin, which dynamically queries VMware APIs and tells Ansible what nodes can be managed. 

More Information on Ansible & VMWare: 
- `VMWare Inventory <https://docs.ansible.com/ansible/latest/scenario_guides/vmware_scenarios/vmware_inventory.html>`

A particular scenario within VATER where the interaction between Ansible and VMWare is relevant includes utilizing Ansible to clone a VM from already existing VMware template: 
- 'Cloning VM <https://docs.ansible.com/ansible/latest/scenario_guides/vmware_scenarios/scenario_clone_template.html>`
   
More Information on Ansible: 
- `Ansible VMware Guide <https://docs.ansible.com/ansible/latest/scenario_guides/guide_vmware.html>`__
-  `Primary Ansible reference for VMware <https://docs.ansible.com/ansible/latest/collections/community/vmware/index.html#scenario-guide>`
   
Ansible Playbooks
=================
If you need to execute a task with Ansible more than once, the developer can write a playbook. The playbook can push out new configuration or confirm the configuration of remote systems.

In the context of VATER, this will allow the same task to be pushed out to multiple VMs at the same time, allowing for efficient and consistent updates.

A playbook is composed of one or more ‘plays’ in an ordered list. Each play executes part of the overall goal of the playbook, running one or more tasks. Each task calls an Ansible module.  Playbooks with multiple ‘plays’ can orchestrate multi-machine deployment. A Play wil define two things:
- The managed nodes to target, using a pattern
- The task(s) to execute

When a task has executed on all target machines, Ansible moves on to the next task. Within each play, Ansible applies the same task directives to all hosts. If a task fails on a host, Ansible takes that host out of the rotation for the rest of the playbook. At the bottom of the playbook execution, Ansible provides a summary of the nodes that were targeted and how they performed. Most Ansible modules check whether the desired final state has already been achieved, and exit without performing any actions if that state has been achieved, so that repeating the task does not change the final state.

More Information on Playbooks: 
-  `Playbooks <https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html>`

-  `Playbook Keywords <https://docs.ansible.com/ansible/latest/reference_appendices/playbooks_keywords.html>`

-  `AWK Playbooks for vCenter <https://www.robvit.com/ansible-tower-awx/ansible-vmware-playbook-examples/>`

-  `Implicit localhost <https://docs.ansible.com/ansible/2.6/inventory/implicit_localhost.html>`


