from parser import Parser
from config import Config
from gitea import Gitea
import getpass

def main():
    p = Parser()
    c = Config(p.args.configPath)
    p.completeParser(c.cfg["service_list"])

    g = Gitea(c)
    
    while(not g.login(config_password=passwd)):
        passwd = getpass.getpass(prompt="Password: ")

    g.setup()    
        
if __name__ == "__main__":
    main()
