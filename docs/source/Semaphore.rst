Purpose of Semaphore
--------------------

Semaphore provides a GUI that Instructors and Developers can use to
interact with ansible playbooks.
`Website <https://ansible-semaphore.com/>`__

Dashboard Display
-----------------

Runs on ``control`` port ``4000``.

Access via web browser of choice: ``x.x.x.x:4000``

Relevant Task Templates
-----------------------

From the ``Management`` project, task templates are:

::

   Build ISOs
   Build VMs
   Create Class
   Destroy Class

Within a ``Class`` project, task templates are:

::

   Create Range
   Destroy Range
   Revert VM
   Reset VM
   Rebuild VM
   Other Enclave Specific Actions

Create Class
------------

To create a class click the run button on the right side of the screen.
A popup will appear asking you to enter the class number and the number
of students in the task template. The class number must start with a ‘U’
for UCWT or a ‘C’ for CWO. The number of students must **not** have a
leading zero.

After successfully running ``Create Class`` template, refresh the
browser. The new class will appear as a project in the top left.

Troubleshooting Tips
--------------------

If a task fails, the first step is to rerun the task. Occasionally with
large builds instructions are not processed by ``vsphere`` properly and
a 2nd attempt will correct this problem.

If not please create a new issue describing the task you were attempting
and the error message
