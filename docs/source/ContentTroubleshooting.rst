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

--> vsphere-iso.win_10_wkst3: File [neo-ds01] win_10_wkst3_template_1/<sensitive>-tmp-created-floppy.flp was not found ` - if you see this error restart the build and the second attempt is likely to build properly.

Tips for Using the File Provisioner
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When using the file provisioner to move files, the file source and destination must be explicitly stated on each file being moved. Complications arise when trying to move entire directories; packer puts the files in a random temp folder and the files will not appear in the desired location.

--Note: This only applies to packer. If moving files or directories after the packer template creation process is complete, disregard these steps and move the files/directories normally.

Working with Windows
^^^^^^^^^^^^^^^^^^^^
Use Windows System Image Manager to create and verify answer files. Windows 10 has the Administrator account disabled by default - if enabled, it can break parts of your build process. Set packer to winrm into the box you're building via the Administrator account if you need complete access (ex. installing vmware-tools)

In the case the Destroy Class does not function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Go to Settings > Delete Project (big red button) This doe NOT delete the
range and Destroy Range should still function separately.


Server Error
^^^^^^^^^^^^
Build 'vsphere-iso.windows' errored after 5 seconds 60 milliseconds: ServerFaultCode: Cannot complete login due to an incorrect user name or password. 

- If these error occurs when attempting and builds - verify vCenter credentials


Limit to parallel builds
^^^^^^^^^^^^^^^^^^^^^^^

Parallel builds, while time efficient are resource intensive - current
resources prevent **>4** parallel builds - more builds attempted will
fail due to memory usage.

Terraform
~~~~~~~~~

Lock State Errors
^^^^^^^^^^^^^^^^^

Terraform uses state locks to prevent multiple users from modifying the
same terraform resources at once. If a task terminates prematurely or is
completed unsuccessfully, terraform may not release the state lock,
which causes errors. To forcibly kill the terraform processes holding
state locks run these commands.

::

   ps -ef | fgrep terraform | awk '{print $2}' | tee /tmp/pids
   sudo kill $(cat /tmp/pids)

or ``sudo killall terraform``

Hanging Tasks
^^^^^^^^^^^^^

If semaphore is hanging and not showing helpful errors or warnings,
`plan <https://www.terraform.io/cli/commands/plan>`__ and
`apply <https://www.terraform.io/cli/commands/apply>`__ are two helpful
Terraform CLI commands. ``terraform plan -out fileName`` and
``terraform apply "fileName"`` allow for troubleshooting terraform
specifically and in a more isolated manner. The ``plan`` command will
ask for inputs to define variables - these can be found in
``groupvars/all/folderOfThingToDebug`` along with the global var files

Note: vm path should be ``class/student`` aka the prev 2 answers
combined give you the final answer.


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


