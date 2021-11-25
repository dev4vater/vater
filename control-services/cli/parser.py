import argparse

class Parser():
    def __init__(self):

        # Create the parser and disable help messages--
        #   they'll be built later
        self.__parser = argparse.ArgumentParser(
            add_help = False
        )

        # The path to the configuration file, used
        #   to setup the rest of the parser
        self.__parser.add_argument(
            '-c', '--configPath',
            help =  'The json conifguration file',
            default = '../config.json'
        )

        # Grab the configuration path without completely
        #   parsing argumnets
        self.args = self.__parser.parse_known_args()[0]

    # Complete the setup of the parser with values from
    #   the configuration file
    def completeParser(self, services):

        # Subcommand help headers
        self.__subparsers = self.__parser.add_subparsers(
            help = 'Sub-command help'
        )

        ### Init subparser
        self.__parser_init = self.__subparsers.add_parser(
            'init',
            description =   'Must be run before other commands.'
                            ' Validates the configuration and'
                            ' sets up the specified services',

            help =  'Must be run before other commands'
        )

        ### Task subparser
        self.__parser_task = self.__subparsers.add_parser(
            'task',
            description =   'Executes a task in Semaphore',
            help =  'Executes a task in Semaphore'
        )

        self.__parser_task.add_argument(
            '-n', '--name',
            help = 'A class name formatted class#####',
            required = True
        )

        self.__parser_task.add_argument(
            '-s', '--size',
            help = 'The size of the class',
            required = True
        )

        ### Sync subparser
        self.__parser_sync = self.__subparsers.add_parser(
            'sync',
            description =   'Syncs the upstrea content repository'
                            ' with the Gitea content repository',
            help =  'Syncs the upstrea content repository'
                    ' with the Gitea content repository'
        )

        ### Stop subparser
        self.__parser_stop = self.__subparsers.add_parser(
            'stop',
            description =   'Stops containers',
            help =  'Stops containers',
        )

        self.__parser_stop.add_argument(
            'service',
            help = 'A service defined in the configuration file',
            choices = services, 
            default = 'all'
        )
        
        ### Restart subparser
        self.__parser_restart = self.__subparsers.add_parser(
            'restart',
            description =   'Stops containers, prunes dangling Docker'
                            ' artifacts, and then starts containers',
            help =  'Stops containers, prunes dangling Docker'
                    ' artifacts, and then starts containers',
        )

        self.__parser_restart.add_argument(
            'service',
            help = 'A service defined in the configuration file',
            choices = services, 
            default = 'all'
        )

        ### Clean subparser
        self.__parser_clean = self.__subparsers.add_parser(
            'clean',
            description =   'Stops containers, force removal of'
                            ' all Docker artifacts, and deletes'
                            ' the data directory',
            help =  'Stops containers, force removal of'
                    ' all Docker artifacts, and deletes'
                    ' the data directory',
        )

        self.__parser_clean.add_argument(
            'service',
            help = 'A service defined in the configuration file',
            choices = services, 
            default = 'all'
        )

        # Access subparser
        self.__parser_access = self.__subparsers.add_parser(
            'access',
            description =  'Provides a bash prompt into a service',
            help =  'Provides a bash prompt into a service'
        )

        # Help was disabled when the parser was instantiated, 
        #   so rebuild it now
        self.__parser.add_argument(
            '-h', '--help',
            help= 'show this help message and exit',

            action='help',
            default='==SUPPRESS=='
        )

        # Process added arguments
        self.args = self.__parser.parse_args()
