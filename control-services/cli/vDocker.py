import threading
import subprocess

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

        subprocess.check_output(cmd, universal_newlines=True)

    def compose_stop(self, containers):
        containers = self.__makeStrList(containers)

        cmd = self.composePreface + [
                'stop'
            ] + containers

        subprocess.check_output(cmd, universal_newlines=True)

    def system_prune(self):

        cmd = self.dockerPreface + [
                'system',
                'prune', '-f'
            ]

        subprocess.check_output(cmd, universal_newlines=True)

    def system_prune_all(self):

        cmd = self.dockerPreface + [
                'system',
                'prune', '-a', '-f'
            ]

        subprocess.check_output(cmd, universal_newlines=True)

    def dexec(self, container, dockerCmd):
        container = self.__makeStrList(container)
        dockerCmd = self.__makeStrList(dockerCmd)

        cmd = self.dockerPreface + [
                'exec',
                ] + container + dockerCmd

        out = subprocess.check_output(cmd, universal_newlines=True)
        return out

    def access(self, container, shell):
        container = self.__makeStrList(container)
        shell = self.__makeStrList(shell)

        cmd = self.dockerPreface + [
            'exec', '-it'
            ] + container + shell

        print('Access initiated-- there is no bash prompt')
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        t = threading.Thread(target=self.__output_reader, args=(p,))
        t.start()

        t.join()

    def __makeStrList(self, s):
        if isinstance(s, str):
            s = list(s.split('~'))
        return s

    def __output_reader(self, proc):
        for line in iter(proc.stdout.readline, b''):
            print('{0}'.format(line.decode('utf-8')), end='')
