from parser import Parser
from config import Config
from gitea import Gitea
from semaphore import Semaphore, SemaphoreTaskArgumentError
from vDocker import VDocker
from os import system
import getpass as gp


def main():
    p = Parser()
    c = Config()
    p.completeParser(c.cfg["service_list"])
    if p.args.command == "init":
        init(c, p.args)
    elif p.args.command == "task":
        task(c, p.args)
    elif p.args.command == "sync":
        sync(c, p.args)
    elif p.args.command == "config":
        config(c, p.args)
    elif p.args.command == "stop":
        stop(c, p.args)
    elif p.args.command == "restart":
        restart(c, p.args)
    elif p.args.command == "clean":
        clean(c, p.args)
    elif p.args.command == "access":
        access(c, p.args)
    elif p.args.command == 'kill':
        killTerraform(c, p.args)


def init(config, args):
    return


def task(config, args):
    s = Semaphore(config)
    loginSemaphore(s)
    if args.semaphoreCommand == "run":
        try:
            taskOutput = s.runTask(
                args.projectName, args.templateAlias, taskParams=args.taskParams
            )
            print(taskOutput)
        except SemaphoreTaskArgumentError as e:
            print(e)


def sync(config, args):
    g = Gitea(config)
    loginGitea(g)
    g.syncContentRepo(args.branch)


def config(config, args):
    print(config)


def stop(config, args):
    if args.service == "all":
        args.service = config.cfg["service_list"]

    services = []
    services.append(args.service)

    for service in services:
        if service == "gitea":
            g = Gitea(config)
            g.stop()

        if service == "semaphore":
            s = Semaphore(config)
            s.stop()


def restart(config, args):
    services = []

    if args.service == "all":
        services.extend(config.cfg["service_list"])
    else:
        services.append(args.service)

    for service in services:
        if service == "gitea":
            g = Gitea(config)
            g.restartContainer()
            loginGitea(g)
            g.setup()
        if service == "semaphore":
            s = Semaphore(config)
            s.restartContainer()
            loginSemaphore(s)
            s.setup()


def clean(config, args):
    services = []

    if args.service == "all":
        services.extend(config.cfg["service_list"])
    else:
        services.append(args.service)

    for service in services:
        if service == "gitea":
            g = Gitea(config)
            g.clean()
        if service == "semaphore":
            s = Semaphore(config)
            s.clean()


def access(config, args):
    if args.service == "gitea":
        g = Gitea(config)
        g.access()
    elif args.service == "gitea_db":
        print("Not implemented")
        return
    elif args.service == "semaphore":
        s = Semaphore(config)
        s.access_semaphore()
    elif args.service == "semaphore_db":
        s = Semaphore(config)
        s.access_semaphore_db()



def killTerraform(config, args):
    savePIDs = "pgrep terraform | tee /tmp/pids"
    killPIDs = "sudo kill $(cat /tmp/pids)"
    if system("pgrep terraform") == 0:
        system(savePIDs)
        if system(killPIDs) == 0:
            print("successfully killed terraform processes")
    else:
        print("No terraform processes found")


def loginGitea(g):
    while True:
        password = gp.getpass(prompt="Gitea Password: ")
        if g.login(password=password):
            break


def loginSemaphore(s):
    while True:
        password = gp.getpass(prompt="Semaphore Password: ")
        if s.login(password=password):
            break


if __name__ == "__main__":
    main()
