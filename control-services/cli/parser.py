import argparse
import copy
from collections import OrderedDict
import os
import subprocess
import getpass

class Parser():
    def __init__(self):

        # Create the parser and disable help messages--
        #   they'll be built later
        self.__parser = argparse.ArgumentParser(
            add_help = False
        )

        # The path to the configuration file, used
        #   to setup the rest of the parser

        self.homedir = "/home/" + getpass.getuser()

        self.__parser.add_argument(
            '-c', '--configPath',
            help =  'The json conifguration file',
            default = self.homedir + '/vater/control-services/config.json'
        )

        # The path to the env file, used
        #   when executing commands with docker-compose
        self.__parser.add_argument(
            '-e', '--envPath',
            help =  'The json conifguration file',
            default = self.homedir + '/vater/control-services/.env'
        )

        # Grab the configuration path without completely
        #   parsing argumnets
        self.args = self.__parser.parse_known_args()[0]

    # Complete the setup of the parser with values from
    #   the configuration file
    def completeParser(self, services):
        container_choices = copy.deepcopy(services)

        unique_service_choices = []
        for service in services:
            s = service.split('_')[0]
            unique_service_choices.append(s)

        unique_service_choices = list(OrderedDict.fromkeys(unique_service_choices))

        # Subcommand help headers
        self.__subparsers = self.__parser.add_subparsers(
            help = 'Sub-command help',
            dest = 'command'
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
            help = 'Executes a task in Semaphore'
        )

        self.__parser_task.add_argument(
            '--project',
            dest = 'projectName',
            help = 'The name of the project where the task will execute (e.g. "Class 21012" or "Management")',
        )

        self.__parser_task.add_argument(
            '--template',
            dest = 'templateAlias',
            help = 'The alias of the task template to execute (e.g. "Create Range"). Requires specifying the \
                    project with the --project option',
        )

        # TODO: Currently not supported because semaphore does not allow passing parameters in to task template on a per-run basis
        # self.__parser_task.add_argument(
        #    'taskParams',
        #    nargs='*',
        #    help = 'Parameters required by the task in key=value format (e.g. class=21012)'
        # ) 
        
        ### Sync subparser
        self.__parser_sync = self.__subparsers.add_parser(
            'sync',
            description =   'Syncs the upstream content repository'
                            ' with the Gitea content repository',
            help =  'Syncs the upstream content repository'
                    ' with the Gitea content repository'
        )

        branches = subprocess.check_output(
            [
                "git", "--git-dir",
                self.homedir + "/rous/.git",
                "branch", "-r", "--no-color"
            ]
        )

        branches = branches.decode(encoding='utf-8').split()
        unique_branches = []

        for i in branches:
            unique_branches.append(i.replace('origin/',''))

        unique_branches = list(set(unique_branches))
        unique_branches.remove("HEAD")
        unique_branches.remove("->")
        self.__parser_sync.add_argument(
            '-b', '--branch',
            help = 'Specify a github branch in rous to sync to gitea',
            choices = unique_branches,
            default = 'main'
        )

        ### Config subparser
        self.__parser_config = self.__subparsers.add_parser(
            'config',
            description =   'Prints the current configuration',
            help =  'Prints the current configuration'
        )

        ### Stop subparser
        self.__parser_stop = self.__subparsers.add_parser(
            'stop',
            description =   'Stops containers',
            help =  'Stops containers',
        )

        self.__parser_stop.add_argument(
            '-s', '--service',
            help = 'A service defined in the configuration file',
            choices = container_choices + ['all'],
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
            '-s', '--service',
            help = 'A service defined in the configuration file',
            choices = unique_service_choices + ['all'],
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
            '-s', '--service',
            help = 'A service defined in the configuration file',
            choices = container_choices + ['all'],
            default = 'all'
        )

        # Access subparser
        self.__parser_access = self.__subparsers.add_parser(
            'access',
            description =  'Provides a bash prompt into a container',
            help =  'Provides a bash prompt into a container'
        )

        self.__parser_access.add_argument(
            '-s', '--service',
            help = 'A service defined in the configuration file',
            choices = container_choices, 
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

    def error(self, message):
        self.__parser.error(message)
