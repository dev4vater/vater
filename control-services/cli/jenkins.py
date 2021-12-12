from subprocess import check_output
from vDocker import VDocker
from pathlib import Path
import json
import copy
import yaml

class Jenkins():
    def __init__(self, configs):
        self.docker = VDocker(configs)
        self.cfg = configs.cfg

        with open(self.cfg['jenkins']['casc_file_path'], 'w') as cascFile:
            yaml.dump(self.cfg['jenkins']['casc'], cascFile)

    def restart(self):
        container = ['jenkins']

        self.docker.compose_stop(container)
        self.docker.compose_up(container)

    def access(self):
        container = ['jenkins']

        self.docker.access(
            container, '/bin/sh'
        )

    def clean(self):
        container = ['jenkins']

        self.docker.compose_stop(container)
        self.docker.system_prune_all()

    def stop(self):
        return
