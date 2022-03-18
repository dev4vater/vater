Management & Troubleshooting
============================

Packer
~~~~~~~

Naming Conventions
^^^^^^^^^^^^^^^^^^^

All outputs from ``packer`` builds will be named ENCLAVENAME_DEVICENAME
and will be placed in a ``PACKER_TEMPLATES`` folder at the root of the
``VSphere`` datastore.

Troubleshooting Packer Builds
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When building packer templates - the ``--force`` option deletes previous
build artifacts. To circumvent loss of development progress, a good
development practice is to alternate between a ``production folder`` and
a ``testing folder``. Once “testing” completes sucessfully, you can
``packer build --force`` with confidence in the ``production folder``.
The easiest way to do that is with a ``-var`` argument to override the
``vcenter_folder`` variable:

ex.
``packer build --only vsphere-iso.machine --var-file machine.pkrvars.hcl -var vcenter_folder="test" .``

Tips for Using the File Provisioner
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When using the file provisioner to move files, the file source and destination must be explicitly stated on each file being moved. Complications arise when trying to move entire directories; packer puts the files in a random temp folder and the files will not appear in the desired location.

--Note: This only applies to packer. If moving files or directories after the packer template creation process is complete, disregard these steps and move the files/directories normally.

In the case the Destroy Class does not function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Go to Settings > Delete Project (big red button) This doe NOT delete the
range and Destroy Range should still function separately.


Server Error
^^^^^^^^^^^^
Build 'vsphere-iso.windows' errored after 5 seconds 60 milliseconds: ServerFaultCode: Cannot complete login due to an incorrect user name or password. 

- If these error occurs when attempting and builds - verify vCenter credentials


Ansible 
~~~~~~~

Referencing group_vars
^^^^^^^^^^^^^^^^^^^^^^

The ansible playbooks are located in ``rous/tasks``. These playbooks use
variables located in YAML format in ``rous/tasks/group_vars/all/*.yml``
files. Ansible by default looks for variables in ``group_vars/all``
`folder <https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html>`__.
To reference the variables in playbooks, you use
TOPLEVEL.NEXTLEVEL.VARIABLENAME with as many nested levels required to
fully define the variable.

Using ansible to take actions on individual VMs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The module is called `community.vmware.wmware_vm_shell` it uses a unique vm_id to reference the vm.  Current VM naming conventions ensure that the vm name is a uid, but moids ect. can be used as well.  Specifying a folder and a vm name fails as a unique id.  The `vm_shell_cwd` option fails to work as advertised on windows 2019.  Had to specify the absolute path of a script to run it.


Gitea
~~~~~

Troubleshooting Gitea
^^^^^^^^^^^^^^^^^^^^^

``gitea`` hosts a local copy of a branch of code located in the ``rous``
repository. In ``gitea`` the branch is called ``master``. By using the
``vater sync -b <branch name>`` command, any specified branch of the
``rous`` repository is copied into ``gitea``.

If this is not successful use the CLI to clean and restart the service:

``vater clean -s semaphore`` then ``vater restart -s semaphore``
(**After cleaning** - restarting will take about 10min to rebuild the
docker container)

Semaphore
~~~~~~~~~

Removing repositories from Semaphore
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When semaphore runs it will create a copy of the ``gitea`` repository
named ``repository_project#_#``. This repository should be updated
anytime the code changes in ``gitea``. If it fails to update, you can
access the docker host with this command \_________. Then navigate to
``/tmp/semaphore`` and run the command ``rm -rf repository_project#_#``
Rerunning the task template will cause semaphore to make a new copy of
the code in gitea


Using Chocolatey
~~~~~~~~~~~~~~~~~

Commands 
^^^^^^^

We install and use ``chocolatey`` as a windows package manager. Below
are listed some useful commands and options for making sure software is
installed properly. **Run as Administrator or from an elevated shell**

``clist --local-only`` - lists all packages installed

``choco install <programName> -y`` - installs program answering
affirmative to all prompts

``choco install --allowunofficial <programName> --version=<X.X.X> -y`` -
allows unlisted installation, use if using an installer that hasn’t been
approved by ``chocolatey`` moderators (NetworkMiner 2.7.2 is an example
of where this is needed)

``choco install <programName> -n`` - download package and “install”
without actually installing, finish installation by running the
installation script in
``C:\ProgramData\chocolatey\lib\<programName>\tools``

