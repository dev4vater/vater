from parser import Parser
from config import Config
from gitea import Gitea
import getpass as gp

def main():
    p = Parser()
    c = Config(p.args.configPath)
    p.completeParser(c.cfg["service_list"])

    if p.args.command == 'init':
        init(c, p.args)
    elif p.args.command == 'task':
        task(c, p.args)
    elif p.args.command == 'sync':
        sync(c, p.args)
    elif p.args.command == 'stop':
        stop(c, p.args)
    elif p.args.command == 'restart':
        restart(c, p.args)
    elif p.args.command == 'clean':
        clean(c, p.args)
    elif p.args.command == 'access':
        access(c, p.args)

def init(config, args):
    return

def task(config, args):
    return

def sync(config, args):
    g = loginGitea(config)
    g.syncContentRepo()

def stop(config, args):
    if args.service == 'all':
        args.service = config.cfg['service_list']

    if args.service == 'gitea':
        g = loginGitea(config)
        
    if service == 'semaphore':
        return

def restart(config, args):
    if args.service == 'all':
        args.service = config.cfg['service_list']

    services = []
    services.append(args.service)

    for service in services:
        if service == 'gitea':
            g = Gitea(config)
            g.restartContainer()
            loginGitea(g, config)
            g.setup()
        if service == 'semaphore':
            return

def clean(config, args):
    if args.service == 'all':
        args.service = config.cfg['service_list']

    services = []
    services.append(args.service)
    for service in services:
        if args.service == 'gitea':
            g = Gitea(config)
            g.clean()
        if service == 'semaphore':
            return

def access(config, args):
    if args.service == 'gitea':
        return
    elif args.service == 'gitea_db':
        print('Not implemented')
        return
    elif args.service == 'semaphore':
        return
    elif args.service == 'semaphore_db':
        return

def loginGitea(g, config):
    while True:
        password = gp.getpass(prompt='Password: ')
        if(g.login(config_password=password)):
            break

if __name__ == "__main__":
    main()
