from parser import Parser
from config import Config
from jenkins import Jenkins
from gitea import Gitea
from semaphore import Semaphore, SemaphoreTaskArgumentError
from vDocker import VDocker
import getpass as gp

def main():
    p = Parser()
    c = Config(p.args.configPath, p.args.envPath)
    p.completeParser(c.cfg["service_list"])
    try:
        if p.args.command == 'init':
            init(c, p.args)
        elif p.args.command == 'task':
            task(c, p.args)
        elif p.args.command == 'sync':
            sync(c, p.args)
        elif p.args.command == 'config':
            config(c, p.args)
        elif p.args.command == 'stop':
            stop(c, p.args)
        elif p.args.command == 'restart':
            restart(c, p.args)
        elif p.args.command == 'clean':
            clean(c, p.args)
        elif p.args.command == 'access':
            access(c, p.args)
    except CommandArgumentsError as e:
        p.error(e)
    

def init(config, args):
    return

def task(config, args):
    # Use optional arguments so task status checking can be implemented as a future feature enhancement
    if args.templateAlias is not None:
        runSemaphoreTask(config, args)

def runSemaphoreTask(config, args): 
    s = Semaphore(config)
    if args.projectName is None:
        raise CommandArgumentsError('Use of the --template option requires specifying a project. See "vater task -h"') 
    try:
        loginSemaphore(s)
        taskOutput = s.runTask(
            args.projectName, args.templateAlias
        )
        print(taskOutput)
    except Exception as e:
        print(e)

def sync(config, args):
    g = Gitea(config)
    loginGitea(g)
    g.syncContentRepo(args.branch)

def config(config, args):
    print(config)

def stop(config, args):
    if args.service == 'all':
        args.service = config.cfg['service_list']

    services = []
    services.append(args.service)

    for service in services:
        if service == 'gitea':
            g = Gitea(config)
            g.stop()

        if service == 'semaphore':
            s = Semaphore(config)
            s.stop()

def restart(config, args):
    services = []

    if args.service == 'all':
        services.extend(config.cfg['service_list'])
    else:
        services.append(args.service)

    for service in services:
        if service == 'gitea':
            g = Gitea(config)
            g.restartContainer()
            loginGitea(g)
            g.setup()
        if service == 'semaphore':
            s = Semaphore(config)
            s.restartContainer()
            loginSemaphore(s)
            s.setup()
        if service == 'jenkins':
            j = Jenkins(config)
            j.restart()

def clean(config, args):
    services = []

    if args.service == 'all':
        services.extend(config.cfg['service_list'])
    else:
        services.append(args.service)

    for service in services:
        if service == 'gitea':
            g = Gitea(config)
            g.clean()
        if service == 'semaphore':
            s = Semaphore(config)
            s.clean()
        if service == 'jenkins':
            j = Jenkins(config)
            j.clean()

def access(config, args):
    if args.service == 'gitea':
        g = Gitea(config)
        g.access()
    elif args.service == 'gitea_db':
        print('Not implemented')
        return
    elif args.service == 'semaphore':
        s = Semaphore(config)
        s.access_semaphore()
    elif args.service == 'semaphore_db':
        s = Semaphore(config)
        s.access_semaphore_db()
    elif args.service == 'jenkins':
        j = Jenkins(config)
        j.access()

def loginGitea(g):
    while True:
        password = gp.getpass(prompt='Gitea Password: ')
        if(g.login(password=password)):
            break

def loginSemaphore(s):
    while True:
        password = gp.getpass(prompt='Semaphore Password: ')
        if(s.login(password=password)):
            break

class CommandArgumentsError(Exception):
    """Raised when a vater command could not be executed using the given arguments"""
    pass

if __name__ == "__main__":
    main()
