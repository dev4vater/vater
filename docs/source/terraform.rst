Introduction To Terraform
-------------------------

What Is The Design Of Terraform?
--------------------------------

.. image:: https://github.com/uwardlaw/vater/blob/main/diagram/terraformDesign.svg

How to Use Terraform
--------------------

Debugging
~~~~~~~~~

Lock State Errors
^^^^^^^^^^^^^^^^^

Terraform uses state locks to prevent multiple users from modifying the
same terraform resources at once. If a task terminates prematurely or is
completed unsuccessfully, terraform may not release the state lock,
which causes errors. To forcibly kill the terraform processes holding
state locks run these commands

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
combined give you the final answer
