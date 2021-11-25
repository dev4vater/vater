from parser import Parser
from config import Config

def main():
    p = Parser()
    c = Config(p.args.configPath)
    p.completeParser(c.cfg["service_list"])

if __name__ == "__main__":
    main()
