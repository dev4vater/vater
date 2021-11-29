from api import Api
from subprocess import check_output
from pathlib import Path
import glob
import json
import copy

class Semaphore():
    def __init__(self, configs):
        self.api = Api()
        self.cfg = configs.cfg 
        self.wasTokenGenerated = False

    def login(self, password=None):
        if password is None:
            password=self.cfg['semaphore']['password']

        envPath = self.cfg['docker']['env_path']
        with open(envPath, "r") as f:
            lines = f.readlines()
            with open(envPath, "w") as f:
                for line in lines:
                    if 'semaphore_admin_password' not in line.strip("\n"):
                        f.write(line)
                f.write('semaphore_admin_passowrd=' + password + '\n')

        r = self.api.s.post(
                url=self.cfg['semaphore']['api']['login'],
                data = (
                    '{'
                        '"auth": "' + self.cfg['semaphore']['user'] + '", '
                        '"password": "' + self.cfg['semaphore']['password'] + '"'
                    '}'    
                )   
            )     

        if r.status_code == 401:
            return False

        r = self.api.get(
                url=self.cfg['semaphore']['api']['tokens']
            )

        self.activeToken = ''

        tokens = json.loads(r.text)
        for token in tokens:
            if token["expired"] == False:
                self.activeToken = token['id']

        if self.activeToken == '':
            r = self.api.post(
                    url=self.cfg['semaphore']['api']['tokens'],
                )
            self.wasTokenGenerated = True
            self.activeToken = json.loads(r.text)['id']
        
        return True

    def runTask(self):
        return

    def restartContainer(self):
        return

    def access(self):
        return

    def clean(self):
        return

    def stop(self):
        return

    def setup(self):
        # Create the management project
        name = 'Management'
        self.managementProjectId = self.__createItemAndID(
            name = name,
            url=self.cfg['semaphore']['api']['projects'],
            data = (
                '{'
                    '"name": "' + name + '", '
                    '"alert": false'
                '}'
            )
        )

        # Update the URLs with the new project ID
        self.__updateApiUrlsManagementId()
        
        # Create Key of type None
        name = 'NoneKey'
        self.noneKeyId = self.__createItemAndID(
            name = name,
            url=self.cfg['semaphore']['api']['project_keys'],
            data = (
                '{'
                    '"name": "' + name + '", '
                    '"type": "None", '
                    '"project_id": "' + str(self.managementProjectId) + '", '
                '}'
            )
        )

        name = 'NoneKeyLP'
        self.noneKeyLPId = self.__createItemAndID(
            name = name,
            url=self.cfg['semaphore']['api']['project_keys'],
            data = (
                '{'
                    '"name": "' + name + '", '
                    '"type": "login_password", '
                    '"login_password": '
                        '{'
                            '"login": "", '
                            '"password": "none" '
                        '}, '
                    '"project_id": "' + str(self.managementProjectId) + '", '
                '}'
            )
        )

        # Create content repo
        name = 'Playbooks'
        self.repositoryId = self.__createItemAndID(
            name = name,
            url=self.cfg['semaphore']['api']['project_repos'],
            data = (
                '{'
                    '"name": "' + name + '", '
                    '"project_id": "' + str(self.managementProjectId) + '", '
                    '"git_url": "' + str(self.cfg['gitea']['config_repo_url']) + '", '
                    '"ssh_key_id": ' + str(self.noneKeyId) + ''
                '}'
            )
        )

        # Create vCenter inventory
        self.__createInventory()

        # Create localhost inventory
        self.__createInventory()

        # Create environment
        self.__createEnvironment()

        if self.wasTokenGenerated:
            self.updateEnvironment()
        
        # I don't see where the key semaphore is used, but
        #   it's moved in setup.sh

        self.__copyPrivateKey()

    def __createInventory(self):
        return

    def __createEnvironment(self):
        return

    def __updateEnvironment(self):
        return

    def __createTaskTemplate(self):
        return

    def __copyPrivateKey(self):
        return

    # Helper function that checks to see if there is an
    #   item based on it's name and if there is not,
    #   it creates the item from the provided data and
    #   returns the ID
    def __createItemAndID(self, url, name, data):
        id = self.api.getIDFromName(
            url=url,
            key='name', name=name
        )

        if id == None:
            r = self.api.post(url, data)
            id = json.loads(r.text)['id']

        # Turn on with debug option
        print(name + ' ID: ' + str(id))

        return id

    def __updateApiUrlsManagementId(self):
        for key, url in self.cfg['semaphore']['api'].items():
            self.cfg['semaphore']['api'][key] = url.replace(
                '#', str(self.managementProjectId)
            )
#
#    def restartContainer(self):
#        out = check_output(
#            [
#                'sudo', 'docker-compose', 'stop', 
#                'gitea', 'gitea_db'
#            ],
#            universal_newlines=True
#        )
#        out += check_output(
#            [
#                'sudo', 'docker', 'system', 
#                'prune', '-f'
#            ],
#            universal_newlines=True
#        )
#        out += check_output(
#            [
#                'sudo', 'docker-compose', 'up', 
#                '-d', '--build', '--remove-orphans',
#                'gitea', 'gitea_db'
#            ],
#            universal_newlines=True
#        )
#
#        return out
#
#    def access(self):
#        out = check_output(
#            [
#                'sudo', 'docker', 'exec', '-it', 
#                'gitea', '/bin/bash' 
#            ],
#            universal_newlines=True
#        )
#        return out        
#
#    def clean(self):
#        out = check_output(
#            [
#                'sudo', 'docker-compose', 'stop', 
#                'gitea', 'gitea_db' 
#            ],
#            universal_newlines=True
#        )
#
#        out += check_output(
#            [
#                'sudo', 'docker', 'system', 
#                'prune', '-a', '-f' 
#            ],
#            universal_newlines=True
#        )
#
#        cmd = ['sudo', 'rm', '-rf'] +                                           \
#            self.cfg['gitea']['related_data_dirs']    
#
#        out += check_output(
#            cmd,
#            universal_newlines=True
#        )
#
#        return out        
#        
#
#    def setup(self):
#        # Create organization
#        self.__createOrg()
#
#        # Create content repo
#        self.__createContentRepo()
#
#        # Revokes token
#        self.__revokeConfigurationToken()
#
#    def syncContentRepo(self):
#        self.__copyLatestContentRepo()
#        self.api.post(
#            apiPath=self.cfg['gitea']['api']['mirror_sync_url']
#        )
#
#    def __configUserExists(self):
#        # Select the config user from a list of users currently
#        #   available on Gitea. Returns nothing if the user
#        #   does not exist
#        dockerCmd = (
#            'gitea admin user list | grep ' +           
#            self.cfg['gitea']['config_user'] +                               
#            ' | tr -s \' \' | cut -d \' \' -f 2'
#        )        
#
#        out = check_output(
#            [
#                'sudo', 'docker', 'exec', '-it', 'gitea',
#                'su', 'git', 'bash', '-c',
#                '""' + dockerCmd + '""'
#            ],
#            universal_newlines=True
#        )
#
#        userFound = out.strip()
#
#        if userFound != self.cfg['gitea']['config_user']:
#            return False
#        else:
#            return True
#
#    def __createConfigUser(self, config_password=None):
#        if config_password is None:
#            config_password=self.cfg['gitea']['config_password']
#       
#        dockerCmd = (
#            'gitea admin user create --admin'
#            ' --username ' + self.cfg['gitea']['config_user'] + 
#            ' --email ' + self.cfg['gitea']['config_email'] +
#            ' --password ' + config_password + 
#            ' --must-change-password=false'
#        )
#                    
#        out = check_output(
#            [
#                'sudo', 'docker', 'exec', '-it', 'gitea',
#                'su', 'git', 'bash', '-c',
#                '""' + dockerCmd + '""'
#            ],
#            universal_newlines=True
#        )
#                    
#   
#    def __copyLatestContentRepo(self):
#        # Pull from remote to local, assuming local does not have uncommitted changes
#        # git --git-dir /home/control/$CONFIG_REPO_NAME/.git pull
#        out = check_output(
#            [
#                'git', '--git-dir',
#                self.cfg['host']['content_git_dir_path'], 'pull'
#            ],
#            universal_newlines=True
#        )
#
#        # Check to see if an old repo exists in gitea
#        p = Path(self.cfg['gitea']['content_repo_path'])
#        if p.exists():
#
#            # Display a diff of old repo and new repo
#            out += check_output(
#                [
#                    'sudo', 'git', 'diff', '--diff-filter=r', '--name-status',
#                    '--compact-summary', '--color', '--no-index',
#                    self.cfg['gitea']['content_repo_path'],
#                    self.cfg['host']['content_dir_path']
#                ],
#                universal_newlines=True
#            )
#        
#        # sudo rm -rf data/gitea/git/$CONFIG_REPO_NAME
#        out += check_output(
#            [
#                'sudo', 'rm', '-rf', self.cfg['gitea']['content_repo_path']
#            ],
#            universal_newlines=True
#        )
#
#        # Copy repo over for gitea to import
#        # sudo cp -r /home/control/$CONFIG_REPO_NAME/ data/gitea/git/$CONFIG_REPO_NAME/
#        out += check_output(
#            [
#                'sudo', 'cp', '-r', 
#                self.cfg['host']['content_dir_path'],
#                self.cfg['gitea']['content_repo_path']
#            ],
#            universal_newlines=True
#        )
#
#        # Change the branch to what is expected by Semaphore
#        # sudo git --git-dir data/gitea/git/$CONFIG_REPO_NAME/.git branch -m main master
#        out += check_output(
#            [
#                'sudo', 'git', '--git-dir',
#                self.cfg['gitea']['content_repo_git_dir_path'],
#                'branch', '-m', 'main', 'master'
#            ],
#            universal_newlines=True
#        )
#
#        return out
#
#    def __createOrg(self):
#        # Check to see if the Org exists before trying to create it
#        orgID = self.api.getIDFromName(
#            url=self.cfg['gitea']['api']['orgs'],
#            key='username', name='333TRS'
#        )
#
#        if orgID == None:
#            self.api.post(
#                url = self.cfg['gitea']['api']['orgs'],
#                data = (
#                    '{'
#                    '"username": "333TRS"'
#                    '}'
#                )
#            )
#        
#    def __createContentRepo(self):
#        # Check to see if the repo exists before trying to create it            universal_newlines=True
#        repoID = self.api.getIDFromName(
#            url=self.cfg['gitea']['api']['content_repo'],
#            key='name', name=self.cfg['content_repo']['name']
#        )
#
#        if repoID == None:
#            # Ensure the repository is available for migration in Gitea
#            self.__copyLatestContentRepo()
#            self.api.post(
#                url = self.cfg['gitea']['api']['repos_migrate'],
#                data = (
#                    '{' 
#                    '"clone_addr": "' + self.cfg['gitea']['container_content_repo'] + '", ' 
#                    '"private": false, '                                      
#                    '"mirror": true, '                                        
#                    '"mirror_interval": "0h0m0s", '                           
#                    '"repo_name": "' + self.cfg['content_repo']['name']  + '", '                                   
#                    '"repo_owner": "' + self.cfg['gitea']['org_or_user'] + '"'
#                    '}'
#                )
#            )
#
#    # Checks for the configuration token and deletes
#    #   the token if it it exists
#    def __revokeConfigurationToken(self):
#        tokenID = self.api.getIDFromName(
#            url=self.cfg['gitea']['api']['tokens'],
#            key='name', name='configurationToken'
#        )
#
#        if tokenID != None:
#            url = self.cfg['gitea']['api']['tokens'] + '/' + str(tokenID)
#            self.api.delete(url=url)
#
