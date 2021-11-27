from api import Api
from subprocess import check_output
import json

class Gitea():
    def __init__(self, configs):
        self.api = Api()
        self.cfg = configs.cfg 

    def login(self, config_password=None):
        if config_password is None:
            config_password=self.cfg['gitea']['config_password']

        self.api.s.auth = (
            self.cfg['gitea']['config_user'],
            config_password
        )

        if not self.__configUserExists():
            self.__createConfigUser(config_password=config_password)

        # Confirm we can get a list of tokens, which requires auth
        r = self.api.s.get(url=self.cfg['gitea']['api']['tokens'])     

        if not r.status_code == 200:
            return false

        # If the token exists, we have no way of getting the hash
        #   so remove the token
        self.__revokeConfigurationToken()

        # Get a new configuration token
        r = self.api.post(
                url=self.cfg['gitea']['api']['tokens'],
                data= '{"name": "configurationToken"}'
            )

        # Update auth header with new token
        tokenHash = json.loads(r.text)['sha1']
        self.api.s.headers.update({'Authorization': 'Token {tokenHash}'})

        return True

    def restart(self):
        out = check_output(
            [
                'sudo', 'docker-compose', 'stop', 
                'gitea', 'gitea_db'
            ],
            universal_newlines=True
        )
        out += check_output(
            [
                'sudo', 'docker', 'system', 
                'prune'
            ],
            universal_newlines=True
        )
        out += check_output(
            [
                'sudo', 'docker-compose', 'up', 
                '-d', '--build', '--remove-orphans',
                'gitea', 'gitea_db'
            ],
            universal_newlines=True
        )

        self.setup()

        return out


    def setup(self):
        # Create organization
        self.__createOrg()

        # Create content repo
        self.__createContentRepo()

        # Revokes token
        self.__revokeConfigurationToken()

    def syncContentRepo(self):
        self.__copyLatestContentRepo()
        self.api.post(
            apiPath=self.cfg['gitea']['api']['mirror_sync_url']
        )

    def __configUserExists(self):
        # Select the config user from a list of users currently
        #   available on Gitea. Returns nothing if the user
        #   does not exist
        dockerCmd = (
            'gitea admin user list | grep ' +           
            self.cfg['gitea']['config_user'] +                               
            ' | tr -s \' \' | cut -d \' \' -f 2'
        )        

        out = check_output(
            [
                'sudo', 'docker', 'exec', '-it', 'gitea',
                'su', 'git', 'bash', '-c',
                '""' + dockerCmd + '""'
            ],
            universal_newlines=True
        )

        userFound = out.strip()

        if userFound != self.cfg['gitea']['config_user']:
            return False
        else:
            return True

    def __createConfigUser(self, config_password=None):
        if config_password is None:
            config_password=self.cfg['gitea']['config_password']
       
        dockerCmd = (
            'gitea admin user create --admin'
            '--username ' + config_user + 
            '--email ' + self.cfg['gitea']['config_email'] +
            '--password ' + config_password + 
            '--must-change-password=false'
        )
                    
        out = check_output(
            [
                'sudo', 'docker', 'exec', '-it', 'gitea',
                'su', 'git', 'bash', '-c',
                '""' + dockerCmd + '""'
            ],
            universal_newlines=True
        )
                    
   
    def __copyLatestContentRepo(self):
        # Pull from remote to local, assuming local does not have uncommitted changes
        # git --git-dir /home/control/$CONFIG_REPO_NAME/.git pull
        out = check_output(
            [
                'git', '--git-dir',
                self.cfg['gitea']['content_repo_git_dir_path'], 'pull'
            ],
            universal_newlines=True
        )

        # Display a diff of old repo and new repo
        out += check_output(
            [
                'sudo', 'git', 'diff', '--diff-filter=r', '--name-status',
                '--compact-summary', '--color', '--no-index',
                self.cfg['gitea']['content_repo_path'],
                self.cfg['host']['content_dir_path']
            ],
            universal_newlines=True
        )
        
        # sudo rm -rf data/gitea/git/$CONFIG_REPO_NAME
        out += check_output(
            [
                'sudo', 'rm', '-rf', self.cfg['gitea']['content_repo_path']
            ],
            universal_newlines=True
        )

        # Copy repo over for gitea to import
        # sudo cp -r /home/control/$CONFIG_REPO_NAME/ data/gitea/git/$CONFIG_REPO_NAME/
        out += check_output(
            [
                'sudo', 'cp', '-r', 
                self.cfg['host']['content_dir_path'],
                self.cfg['gitea']['content_repo_path']
            ],
            universal_newlines=True
        )

        # Change the branch to what is expected by Semaphore
        # sudo git --git-dir data/gitea/git/$CONFIG_REPO_NAME/.git branch -m main master
        out += check_output(
            [
                'sudo', 'git', '--git-dir',
                self.cfg['gitea']['content_repo_git_dir_path'],
                'branch', '-m', 'main', 'master'
            ],
            universal_newlines=True
        )

        return out

    def __createOrg(self):
        # Check to see if the Org exists before trying to create it
        orgID = self.api.getIDFromName(
            url=self.cfg['gitea']['api']['orgs'],
            key='username', name='333TRS'
        )

        if orgID == None:
            self.api.post(
                url = self.cfg['gitea']['api']['tokens'],
                data = (
                    '{'
                    '"username": "333TRS"'
                    '}'
                )
            )
        
    def __createContentRepo(self):
        # Check to see if the repo exists before trying to create it            universal_newlines=True
        repoID = self.api.getIDFromName(
            url=self.cfg['gitea']['api']['content_repo'],
            key='name', name=self.cfg['content_repo']['name']
        )

        if repoID == None:
            # Ensure the repository is available for migration in Gitea
            self.__copyLatestContentRepo()
            self.api.post(
                url = self.cfg['gitea']['api']['repos_migrate'],
                data = (
                    '{' 
                    '"clone_addr": "' + self.cfg['gitea']['container_content_repo'] + '", ' 
                    '"private": false, '                                      
                    '"mirror": true, '                                        
                    '"mirror_interval": "0h0m0s", '                           
                    '"repo_name": "' + self.cfg['content_repo']['name']  + '", '                                   
                    '"repo_owner": "' + self.cfg['gitea']['org_or_user'] + '"'
                    '}'
                )
            )

    # Checks for the configuration token and deletes
    #   the token if it it exists
    def __revokeConfigurationToken(self):
        tokenID = self.api.getIDFromName(
            url=self.cfg['gitea']['api']['tokens'],
            key='name', name='configurationToken'
        )

        if tokenID != None:
            url = self.cfg['gitea']['api']['tokens'] + '/' + str(tokenID)
            self.api.delete(url=url)

