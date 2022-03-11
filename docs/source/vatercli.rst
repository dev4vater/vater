The VATER CLI is designed so that Instructors and Developers can run
task templates, restart services and access containers from the command
line. All actions that are run from ``Semaphore`` can also be run from
the VATER CLI.

::

   vater -h
   usage: vater.py [-c CONFIGPATH] [-e ENVPATH] [-h] {init,task,sync,config,stop,restart,clean,access} ...

   positional arguments:
     {init,task,sync,config,stop,restart,clean,access}
                           Sub-command help
       init                Must be run before other commands
       task                Executes a task in Semaphore
       sync                Syncs the upstream content repository with the Gitea content repository
       config              Prints the current configuration
       stop                Stops containers
       restart             Stops containers, prunes dangling Docker artifacts, and then starts containers
       clean               Stops containers, force removal of all Docker artifacts, and deletes the data directory
       access              Provides a bash prompt into a container

   optional arguments:
     -c CONFIGPATH, --configPath CONFIGPATH
                           The json conifguration file
     -e ENVPATH, --envPath ENVPATH
                           The json conifguration file
     -h, --help            show this help message and exit

::

   vater init -h
   usage: vater.py init [-h]

   Must be run before other commands. Validates the configuration and sets up the specified services

   optional arguments:
     -h, --help  show this help message and exit

::

   vater task -h
   usage: vater.py task [-h] name classID size

   Executes a task in Semaphore

   positional arguments:
     name        The name of the task to execute
     classID     A class name formatted class#####
     size        The size of the class

   optional arguments:
     -h, --help  show this help message and exit

::

   vater sync -h
   usage: vater.py sync [-h] [-b {uwardlaw/task-vmInput,demo,iss117,main,iss82,iss89,iss150,iss151}]

   Syncs the upstream content repository with the Gitea content repository

   optional arguments:
     -h, --help            show this help message and exit
     -b {uwardlaw/task-vmInput,demo,iss117,main,iss82,iss89,iss150,iss151}, --branch {uwardlaw/task-vmInput,demo,iss117,main,iss82,iss89,iss150,iss151}
                           Specify a github branch in rous to sync to gitea

::

   vater stop -h
   usage: vater.py stop [-h] [-s {gitea,gitea_db,semaphore,semaphore_db,jenkins,all}]

   Stops containers

   optional arguments:
     -h, --help            show this help message and exit
     -s {gitea,gitea_db,semaphore,semaphore_db,jenkins,all}, --service {gitea,gitea_db,semaphore,semaphore_db,jenkins,all}
                           A service defined in the configuration file

::

    vater restart -h
   usage: vater.py restart [-h] [-s {gitea,semaphore,jenkins,all}]

   Stops containers, prunes dangling Docker artifacts, and then starts containers

   optional arguments:
     -h, --help            show this help message and exit
     -s {gitea,semaphore,jenkins,all}, --service {gitea,semaphore,jenkins,all}
                           A service defined in the configuration file

::

    vater clean -h
   usage: vater.py clean [-h] [-s {gitea,gitea_db,semaphore,semaphore_db,jenkins,all}]

   Stops containers, force removal of all Docker artifacts, and deletes the data directory

   optional arguments:
     -h, --help            show this help message and exit
     -s {gitea,gitea_db,semaphore,semaphore_db,jenkins,all}, --service {gitea,gitea_db,semaphore,semaphore_db,jenkins,all}
                           A service defined in the configuration file

::

   vater access -h
   usage: vater.py access [-h] [-s {gitea,gitea_db,semaphore,semaphore_db,jenkins}]

   Provides a bash prompt into a container

   optional arguments:
     -h, --help            show this help message and exit
     -s {gitea,gitea_db,semaphore,semaphore_db,jenkins}, --service {gitea,gitea_db,semaphore,semaphore_db,jenkins}
                           A service defined in the configuration file
