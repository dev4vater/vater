from subprocess import check_output
from vDocker import VDocker
from pathlib import Path
import json
import copy

class Jenkins():
    def __init__(self, configs):
        self.docker = VDocker(configs)

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
