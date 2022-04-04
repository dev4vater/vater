Management & Troubleshooting
============================

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
the code in gitea.

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

