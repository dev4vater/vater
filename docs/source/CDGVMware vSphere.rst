VMware vSphere
==================

Packer
~~~~~~~

Convert Methodology
^^^^^^^^^^^^^^^^^^^

New Development:

- Build out the VM to understand all of the build details
- Find the method of automated installation supported by the Operating System: 
- This can vary from a specific boot command, a preseed.cfg, cloud-init with user-data and meta-data, a ks.cfg, or a windows answer file autounattend.xml

Converting Legacy:
^^^^^^^^^^^^^^^^^^

Build out the VM once to understand the installation specific questions. Research to find where the files holding that installation information might be. Identify all installed programs, files, and user accounts:

1) Base Templates
2) Specify Configuration - Specifications can be added in two main areas: 

    - the automated installation steps via edits to the related files 
    - during the provisioning steps by adding the desired provisioners and related files 
    
Best Practices
^^^^^^^^^^^^^^

- Build or use prebuilt generic builders specifically for your virtualization environment
- Verify the generic template builds properly and then use that as a base to start the specific configuration of the golden template
- When using provisioners, read the recommended use in the packer documentation to understand whether that provisioner will meet your needs
- Provisioners that accept inline commands (Shell, Powershell, etc) can accept long "one-liner" commands, but troubleshooting the build is substantially easier when commands are broken into the smallest possible strings i.e. `inline = ["one action", "another one", "etc"]`
- The `file` provisioner should be used to transfer specific files to exact file locations if the files being transferred will be used later in the packer provisioning process. Otherwise, the file provisioner will move entire directories without issue for access once the template is complete and you have your packer build artifact
- Testing provisioning builds can be the longest process in development - to save time, test the commands and scripts in a 

Tips & Tricks
^^^^^^^^^^^^^

- If no generic packer build exists for your specific operating system and environment, look for a different packer build for your desired operating system - you can then edit the builder based on the desired environment. If this is not available, find related operating systems and use them as a reference to build the generic for your system.
- Use TMUX when developing to allow better management of your build sessions. Build times range from 10 minutes to hours, so being able to keep an eye on the build progress and watch for errors while continuing other work is extremely helpful
- Having a package manager makes provisioning software installations much easier and increases code readability - most *nix flavors have one - for windows, chocolatey is a great option and it's also easy to build a chocolatey package for software you might want that isn't supported already

Terraform
~~~~~~~~~~

Convert Methodology
^^^^^^^^^^^^^^^^^^^^

Terraform code for a new network enclave should be converted into a separate terraform module.  To start create a folder in terraform/modules with the new modules name.  Then write the <module name>.tf file inside the module folder.  Include a `varaibles.tf` file with declarations for all variables used within your terraform module.  Include a copy of `vsphere.tf` in the module folder so terraform can connect with the vsphere cluster.

Existing terraform code can be put in the <module name>.tf file but modifying existing terraform modules in `rous` is likely simpler.  Terraform code is broken into blocks.  Each provider such as vsphere or proxmox has blocks specific to that virtualization platform but the content and function is largely the same.  Common blocks reference VM templates, create standard or distributed switches and port groups, clone a VM from a template and take snapshots. 
 
Best Practices
^^^^^^^^^^^^^^
Terraform is a very powerful tool, but VATER is just using it to clone VMs and build virtual networks.  We are not using the post deployment configuration options, all possible VM configuration has been completed in packer and any remaining actions or scenario injects will be performed using ansible.  Templating VM configurations allows for faster and more consistent range deployments. 

Avoid hardcoding values in `.tf` files, use variables instead.  Variables must be defined in 2 places, within the module they are used and within the top level `variables.tf` file.  Any values provided at run time must have a default value included so if that run time variable is not required for a module terraform will not throw errors for undefined variables.  All variables that are not provided at run time have values defined in `variables.auto.tfvars`.  If template or network names change this is the file to change the values in.  

Within the module `.tf` files avoid creating variables that only combine other variable values.  For example, VM templates are written like this `"${var.win10Wkst1}_template"` and the outputted VM name is `"${var.win10Wkst1}"`.  The quotes allow you to combine variables and strings for any specified value.

Tips & Tricks
^^^^^^^^^^^^^^^

The terraform documentation is accurate and helpful.  It describes how to define all resources and what values terraform accepts.  Existing code in rous includes terraform blocks for single NIC and multiple NIC VMs and pulls most required values from the VM template for consistency.

Ansible Semaphore
~~~~~~~~~~~~~~~~~~

Convert Methodology
^^^^^^^^^^^^^^^^^^^^^

Ansible playbooks use the following structure: 

::
    - hosts: localhost
       tasks:
      
    - name: <task name> 
       <task function name if necessary>
          <task body>
        register: output 

    - name: debug <task name> 
      ansible.builtin.debug:
        var: output

If you're using an ansible playbook to call a different ansible playbook then omit the hosts and tasks lines. 

Most playbooks I found online only contain snippets.  Copying tasks and adding them to this existing structure is the easiest way to incorporate other code into playbooks. 

Best Practices
^^^^^^^^^^^^^^^

All ansible variables are kept in `groupvars/all` and ansible references them automatically when you use the syntax `{{ variable_name }}` in your playbook.  

Tips & Tricks
^^^^^^^^^^^^^^
Ansible playbooks are formatted in YAML.  Here is a helpful YAML checker: https://yamlchecker.com/

Testing
^^^^^^^^^

To run ansible playbooks in semaphore modify `rous/bin/setupNewClass.py` to include the new task.  Within this python script, there is a function to create a task with run time variables and one without run time variables. 

Copy an existing `createTaskTemplate` block and change the task name, ansible playbook and dynamicVars if necessary.  Then any new class created in semaphore will contain your task.

