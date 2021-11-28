from subprocess import check_output

class VDocker():
    def __init__(self, configs):
        self.cfg = configs.cfg
        self.composePreface = [
            'sudo', 'docker-compose', 
            '-f', self.cfg['docker']['compose_file_path'], 
            '--env-file', self.cfg['docker']['env_path']
        ]
        self.dockerPreface = ['sudo', 'docker']

    def compose_up(self, containers):
        containers = self.__makeStrList(containers)

        cmd = self.composePreface + [
                'up', '-d', '--build', '--remove-orphans'
            ] + containers
        
        check_output(cmd, universal_newlines=True)

    def compose_stop(self, containers):
        containers = self.__makeStrList(containers)

        cmd = self.composePreface + ['stop'] + containers
        
        check_output(cmd, universal_newlines=True)

    def system_prune(self):

        cmd = self.dockerPreface + [
                'system', 
                'prune', '-f'
            ]
        
        check_output(cmd, universal_newlines=True)

    def system_prune_all(self):

        cmd = self.dockerPreface + [
                'system', 
                'prune', '-a', '-f'
            ]
        
        check_output(cmd, universal_newlines=True)

    def dexec(self, container, dockerCmd):
        container = self.__makeStrList(container)
        dockerCmd = self.__makeStrList(dockerCmd)

        cmd = self.dockerPreface + [
                'exec',
                ] + container + dockerCmd 
        
        out = check_output(cmd, universal_newlines=True)
        return out

    def __makeStrList(self, s):
        if isinstance(s, str):
            s = list(s.split('~'))
        return s
