Edit Configuration
******************

``config.json`` is used by the CLI to configure the different services
and has various options for users to edit.

.. code:: json

   {
     # Enables the development environment setup, including write access
     #   key creation / installation on Control
     #   and various debugging print messages.
     "dev" : { "enable" : true },

     # This is information about the Control node.
     #   The vater/ directory should sit in project_path
     #   E.g. '/home/control/vater/'
     "host" : {
         "hostname" : "control",
         "project_path" : "/home/control/"
       },
     # Changing the content_repo alters what repository is
     #   used for the different lab environments. ROUS requires
     #   access to the private repository
     "repos" : [ {
           "content_repo" : {
               "ansible_dir" : "ansible",
               "name" : "rous",
               "org_or_user" : "uwardlaw",
               "terraform_dir" : "terraform"
             },
           "vater_repo" : {
               "rel_data_dir" : "control-services/data/",
               "name" : "vater",
               "org_or_user" : "uwardlaw"
             }
         } ],

     # These are the different containers started by Docker on control
     #   Note that the CLI creates options for each unique service
     #   Where serviceA, serviceA_db, and serviceA_web are all serviceA
     #   Components of the same service must follow the naming convention
     #   Where serviceB_component1 and serviceB_component2 are grouped
     #   and handled together by a serviceB.py (see CLI Development for more)

   # Note, the default passwords are only used in dev mode. 
   #   the user is otherwise prompted for a password when using
   #   the CLI
     "services" : [ {
           "gitea" : {
               "config_password" : "config",
               "config_user" : "config",
               "config_email" : "config@example.com",
               "org_or_user" : "333TRS",
               "port" : "3000"
             },
           "gitea_db" : {
               "db_password" : "gitea",
               "db_user" : "gitea",
               "port" : "3305"
             },
           "semaphore" : {
               "password" : "cangetin",
               "port" : "4000",
               "user" : "admin"
             },
           "semaphore_db" : {
               "db_password" : "semaphore",
               "db_user" : "semaphore",
               "port" : "3306"
             }
         } ]
   }
