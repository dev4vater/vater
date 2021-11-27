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
    pass

def task(config, args):
    pass

def sync(config, args):
    pass

def stop(config, args):
    if args.service == 'gitea' or args.service == 'gitea_db':

def restart(config, args):
    if args.service == 'gitea' or args.service == 'gitea_db':
        g = Gitea(config)

        while True:
            password = gp.getpass(prompt='Password: ')
            if(g.login(config_password=password)):
                break

        g.restart()
    if args.service == 'semaphore' or args.service == 'semaphore_db':
        return

def clean(config, args):
    if args.service == 'gitea' or args.service == 'gitea_db':

def access(config, args):
    if args.service == 'gitea' or args.service == 'gitea_db':
        
if __name__ == "__main__":
    main()
