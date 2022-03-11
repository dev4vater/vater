Naming Conventions
------------------

All outputs from ``packer`` builds will be named ENCLAVENAME_DEVICENAME
and will be placed in a ``PACKER_TEMPLATES`` folder at the root of the
``VSphere`` datastore.

Referencing group_vars
----------------------

The ansible playbooks are located in ``rous/tasks``. These playbooks use
variables located in YAML format in ``rous/tasks/group_vars/all/*.yml``
files. Ansible by default looks for variables in ``group_vars/all``
`folder <https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html>`__.
To reference the variables in playbooks, you use
TOPLEVEL.NEXTLEVEL.VARIABLENAME with as many nested levels required to
fully define the variable.

Troubleshooting Gitea
---------------------

``gitea`` hosts a local copy of a branch of code located in the ``rous``
repository. In ``gitea`` the branch is called ``master``. By using the
``vater sync -b <branch name>`` command, any specified branch of the
``rous`` repository is copied into ``gitea``.

If this is not successful use the CLI to clean and restart the service:

``vater clean -s semaphore`` then ``vater restart -s semaphore``
(**After cleaning** - restarting will take about 10min to rebuild the
docker container)

Removing repositories from Semaphore
------------------------------------

When semaphore runs it will create a copy of the ``gitea`` repository
named ``repository_project#_#``. This repository should be updated
anytime the code changes in ``gitea``. If it fails to update, you can
access the docker host with this command \_________. Then navigate to
``/tmp/semaphore`` and run the command ``rm -rf repository_project#_#``
Rerunning the task template will cause semaphore to make a new copy of
the code in gitea

Troubleshooting Packer Builds
-----------------------------

When building packer templates - the ``--force`` option deletes previous
build artifacts. To circumvent loss of development progress, a good
development practice is to alternate between a ``production folder`` and
a ``testing folder``. Once “testing” completes sucessfully, you can
``packer build --force`` with confidence in the ``production folder``.
The easiest way to do that is with a ``-var`` argument to override the
``vcenter_folder`` variable:

ex.
``packer build --only vsphere-iso.machine --var-file machine.pkrvars.hcl -var vcenter_folder="test" .``

In the case the Destroy Class does not function
-----------------------------------------------

Go to Settings > Delete Project (big red button) This doe NOT delete the
range and Destroy Range should still function separately.

Using Chocolatey
----------------

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
