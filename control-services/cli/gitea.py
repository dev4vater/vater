from api import Api
import subprocess
import json

class Gitea():
    def __init__(self, configs):
        self.api = Api()
        self.cfg = config 

    def login(
        config_password=self.cfg['gitea']['config_password']
    ):
        self.api.s.auth(
            self.cfg['gitea']['config_user'],
            config_password
        )

        if not self.__configUserExists():
            self.__createConfigUser(config_password=config_password)

        # Confirm we can get a list of tokens, which requires auth
        r = self.api.s.get(url=self.cfg['gitea']['api']['tokens'])     
        if not r.status_code == 200:
            return false

        self.__revokeConfigurationToken()

        # If the token exists, we have no way of getting the hash
        #   so remove the token
        if tokenID != None:
            url = self.cfg['gitea']['api']['tokens'] + '/' + str(tokenID)
            self.api.delete(url=url)

        data = '{"name": "configurationToken"}'
        r = self.api.post(
                url = self.cfg['gitea']['api']['tokens'],
                data = data
            )

        tokenHash = json.loads(response.text)['sha1']
        self.s.headers.update({'Authorization': 'Token {tokenHash})

        return true

    def setup(self):
        # Create organization
        self.__createOrg()

        # Create repo
        self.__createContentRepo()

        # Revoke token
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
        dockerCmd = ('gitea admin user list | grep ' +           
                    config_user +                               
                    ' | tr -s \' \' | cut -d \' \' -f 2')        

        stream = subprocess.Popen(
            ['sudo', 'docker', 'exec', '-it', 'gitea',
            'su', 'git', 'bash', '-c',
            '""' + dockerCmd + '""'
        )

        userFound = stream.read().strip()

        if userFound != config_user:
            return False
        else
            return True

    def __createConfigUser(
        self,
        config_password=self.cfg['gitea']['config_user']
    ):
        dockerCmd = ('gitea admin user create --admin'
                    '--username ' + config_user + 
                    '--email ' + self.cfg['gitea']['config_email'] +
                    '--password ' + config_password + 
                    '--must-change-password=false')
                    
        stream = subprocess.Popen(
            ['sudo', 'docker', 'exec', '-it', 'gitea',
            'su', 'git', 'bash', '-c',
            '""' + dockerCmd + '""' 
        )
                    
   
    def __copyLatestContentRepo(self):
        # Pull from remote to local, assuming local does not have uncommitted changes
        # git --git-dir /home/control/$CONFIG_REPO_NAME/.git pull
        stream = subprocess.Popen(
            ['git', '--git-dir',
            self.cfg['gitea']['content_repo_git_dir_path'], 'pull']
        )

        # Display a diff of old repo and new repo
        stream = subprocess.Popen(
            ['sudo', 'git', 'diff', '--diff-filter=r', '--name-status',
            '--compact-summary', '--color', '--no-index',
            self.cfg['gitea'['content_repo_path'],
            self.cfg['host']['content_dir_path']]
        )
        
        # sudo rm -rf data/gitea/git/$CONFIG_REPO_NAME
        stream = subprocess.Popen(
            ['sudo', 'rm', '-rf', self.cfg['gitea']['content_repo_path']]
        )

        # Copy repo over for gitea to import
        # sudo cp -r /home/control/$CONFIG_REPO_NAME/ data/gitea/git/$CONFIG_REPO_NAME/
        stream = subprocess.Popen(
            ['sudo', 'cp', '-r', 
             self.cfg['host']['content_dir_path'],
             self.cfg['gitea']['content_repo_path']]            
        )

        # Change the branch to what is expected by Semaphore
        # sudo git --git-dir data/gitea/git/$CONFIG_REPO_NAME/.git branch -m main master
        stream = subprocess.Popen(
            ['sudo', 'git', '--git-dir',
            self.cfg['gitea']['content_repo_git_dir_path'],
            'branch', '-m', 'main', 'master']
        )

        return stream

    def __createOrg(self):
        pass
        
    def __createContentRepo(self)
        pass

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

