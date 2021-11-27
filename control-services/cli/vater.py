from parser import Parser
from config import Config
from gitea import Gitea
import getpass as gp

def main():
    p = Parser()
    c = Config(p.args.configPath)
    p.completeParser(c.cfg["service_list"])

    g = Gitea(c)

    while True:
        password = gp.getpass(prompt='Password: ')
        if(g.login(config_password=password)):
            break

    g.setup()    
        
if __name__ == "__main__":
    main()
