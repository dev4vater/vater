from api import Api
from vDocker import VDocker
from subprocess import check_output
from pathlib import Path
import glob
import json
import copy
import pprint
import time

class Semaphore():
    def __init__(self, configs):
        self.api = Api()
        self.cfg = configs.cfg
        self.docker = VDocker(configs)
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
                f.write('semaphore_admin_password=' + password + '\n')

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

    def runTask(self, projectName, templateAlias, taskParams=None):
        projectId = self.__getProjectIdByName(projectName)
        template = self.__getProjectTaskTemplateByAlias(projectId, templateAlias)
        templateId = template['id']
        taskExecutionEnvironment = None
        if taskParams is not None:
            environmentId = template['environment_id']
            templateEnvironment = self.__getProjectEnvironmentById(projectId, environmentId)
            taskExecutionEnvironment = self.__buildTaskEnvironment(taskParams, templateEnvironment)
        
        response = self.__runProjectTaskFromTemplate(projectId, templateId, env=taskExecutionEnvironment)
        
        output = 'Task Created!\nTask ID: ' + str(response['id'])
        return output


    def __getProjectIdByName(self, projectName):
        projectId = self.api.getIDFromName(
            url=self.cfg['semaphore']['api']['projects'],
            key="name", name=projectName
        )

        if projectId is None:
            raise SemaphoreTaskArgumentError('Error: Project "' + projectName + '" not found')
        
        return projectId

    def __getProjectTaskTemplateByAlias(self, projectId, templateAlias):
        templateUrl = self.cfg['semaphore']['api']['project_template'].replace('#', str(projectId))
        projectTemplatesResponse = self.api.get(url=templateUrl)
        projectTemplates = json.loads(projectTemplatesResponse.text)
        foundTemplate = None
        for template in projectTemplates:
            if template['alias'] == templateAlias:
                foundTemplate = template
        
        if foundTemplate is None:
            raise SemaphoreTaskArgumentError('Error: Task template "' + templateAlias + '" not found '
                                             'in the specified project')
        return foundTemplate

    def __getProjectEnvironmentById(self, projectId, environmentId):
        environmentUrl = self.cfg['semaphore']['api']['project_environment'].replace('#', str(projectId))
        environmentUrl += '/' + str(environmentId)
        result = self.api.s.get(url=environmentUrl)
        environmentObject = result.json()
        environmentVariables = json.loads(environmentObject['json']) # the actual key on the API definition is called 'json'
        return environmentVariables

    def __buildTaskEnvironment(self, taskParams, templateEnvironment):
        newEnv = copy.deepcopy(templateEnvironment)
        for param in taskParams:
            if str(param).find('=') == -1:
                raise SemaphoreTaskArgumentError('Error with task parameter "' + param + '". '
                        'Task parameters must be provided in the format of key=value pairs') 
            key = param.split('=')[0]
            value = param.split('=')[1]
            newEnv[key] = value
        return newEnv

    def __runProjectTaskFromTemplate(self, projectId, templateId, env=None):
        taskUrl = self.cfg['semaphore']['api']['project_tasks'].replace('#', str(projectId))
        taskDefinition = { 'template_id': templateId}
        if env is not None:
            taskDefinition['environment'] = json.dumps(env)

        response = self.api.s.post(url=taskUrl, data=json.dumps(taskDefinition))
        return response.json()

    def restartContainer(self):
        containers = ['semaphore', 'semaphore_db']

        self.docker.compose_stop(containers)
        self.docker.compose_up(containers)

    def access_semaphore(self):
        container = ['--user', 'root', 'semaphore']

        self.docker.access(
            container, '/bin/sh'
        )

    def access_semaphore_db(self):
        container = ['semaphore_db']

        self.docker.access(
            container,
                [
                    'mysql',
                    '-u' + self.cfg['semaphore_db']['user'],
                    '-p' + self.cfg['semaphore_db']['password']
                ]
        )

    def clean(self):
        containers = ['semaphore', 'semaphore_db']

        self.docker.compose_stop(containers)
        self.docker.system_prune_all()

        check_output(
            ['sudo', 'rm', '-rf'] +                                             \
            self.cfg['semaphore']['related_data_dirs'],
            universal_newlines=True
        )

    def stop(self):
        return

    def setup(self):
        # Create the management project
        name = 'Management'
        self.managementProjectId = self.__createItemAndID(
            name = name,
            url = self.cfg['semaphore']['api']['projects'],
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
            url = self.cfg['semaphore']['api']['project_keys'],
            data = (
                '{'
                    '"name": "' + name + '", '
                    '"type": "None", '
                    '"project_id": ' + str(self.managementProjectId) + ''
                '}'
            )
        )

        name = 'NoneKeyLP'
        self.noneKeyLPId = self.__createItemAndID(
            name = name,
            url = self.cfg['semaphore']['api']['project_keys'],
            data = (
                '{'
                    '"name": "' + name + '", '
                    '"type": "login_password", '
                    '"login_password": '
                        '{'
                            '"login": "", '
                            '"password": "none" '
                        '}, '
                    '"project_id": ' + str(self.managementProjectId) + ''
                '}'
            )
        )

        # Create semaphore key for using ansible on Control

        with open(self.cfg['semaphore']['private_key'], 'r') as file:
            semaphoreSSHKey = file.read().replace('\n','\\n')
        semaphoreSSHKey = semaphoreSSHKey + '\\n'

        name = 'control'
        self.semaphoreKeyId = self.__createItemAndID(
            name = name,
            url = self.cfg['semaphore']['api']['project_keys'],
            data = (
                '{'
                    '"name": "' + name + '", '
                    '"type": "ssh", '
                    '"ssh": '
                        '{'
                            '"login": "", '
                            '"passphrase": "", '
                            '"private_key": "' +  semaphoreSSHKey + '"'
                        '}, '
                    '"project_id": ' + str(self.managementProjectId) + ''
                '}'
            )
        )

        # Create content repo
        name = 'Playbooks'
        self.repositoryId = self.__createItemAndID(
            name = name,
            url = self.cfg['semaphore']['api']['project_repos'],
            data = (
                '{'
                    '"name": "' + name + '", '
                    '"project_id": ' + str(self.managementProjectId) + ', '
                    '"git_url": "' + self.cfg['gitea']['config_repo_url'] + '", '
                    '"ssh_key_id": ' + str(self.noneKeyId) + ''
                '}'
            )
        )

        # Create vCenter inventory
        name = 'vCenter'
        self.vCenterInvId = self.__createItemAndID(
            name = name,
            url = self.cfg['semaphore']['api']['project_inventory'],
            data = (
                '{'
                    '"name": "' + name + '", '
                    '"project_id": ' + str(self.managementProjectId) + ', '
                    '"inventory": "' + self.cfg['content_repo']['vCenter_inventory_path'] + '", '
                    '"key_id": ' + str(self.noneKeyLPId) + ', '
                    '"ssh_key_id": ' + str(self.noneKeyLPId) + ', '
                    '"type": "file"'
                '}'
            )
        )

        # Create localhost inventory
        name = 'localhost'
        self.localhostInvId = self.__createItemAndID(
            name = name,
            url = self.cfg['semaphore']['api']['project_inventory'],
            data = (
                '{'
                    '"name": "' + name + '", '
                    '"project_id": ' + str(self.managementProjectId) + ', '
                    '"inventory": '
                        '"'
                            '[LOCALHOST]\\n' + self.cfg['host']['ip'] + ''
                        '", '
                    '"key_id": ' + str(self.noneKeyLPId) + ', '
                    '"ssh_key_id": ' + str(self.noneKeyLPId) + ', '
                    '"type": "static"'
                '}'
            )
        )

        # Create localhost inventory
        name = 'control'
        self.controlInvId = self.__createItemAndID(
            name = name,
            url = self.cfg['semaphore']['api']['project_inventory'],
            data = (
                '{'
                    '"name": "' + name + '", '
                    '"project_id": ' + str(self.managementProjectId) + ', '
                    '"inventory": '
                        '"'
                            '[control]\\n' + self.cfg['host']['ip'] + ''
                        '", '
                    '"key_id": ' + str(self.noneKeyId) + ', '
                    '"ssh_key_id": ' + str(self.semaphoreKeyId) + ', '
                    '"type": "static"'
                '}'
            )
        )

        self.env = (
            '"{'
                '\\"api_key\\": \\"' + self.activeToken + '\\",'
                '\\"controlIP\\": \\"' + self.cfg['host']['ip'] + '\\",'
                '\\"playbookRepositoryURL\\": \\"' + self.cfg['gitea']['config_repo_url'] + '\\",'
                '\\"ansiblePathInRepository\\": \\"' + self.cfg['content_repo']['playbook_dir'] + '\\",'
                '\\"vmPathInRepository\\": \\"' + self.cfg['host']['vms_path'] + '\\",'
                '\\"terraformPathInRepositoryOnControl\\": \\"' + self.cfg['host']['terraform_path'] + '\\"'
            '}"'
        )

        # Create environment
        name = 'Env'
        self.envId = self.__createItemAndID(
            name = name,
            url=self.cfg['semaphore']['api']['project_environment'],
            data = (
                '{'
                    '"name": "' + name + '", '
                    '"project_id": ' + str(self.managementProjectId) + ', '
                    '"json": ' + self.env + ''
                '}'
            )
        )

#        print(self.envId)
#
#        print('Checking envId one more time')
#        print(self.api.getIDFromName(url=self.cfg['semaphore']['api']['project_environment'],key='name', name='Env'))
#
#        if self.wasTokenGenerated:
#            self.api.put(
#                url=self.cfg['semaphore']['api']['project_environment'] + (
#                        '/' + str(self.envId)
#                    ),
#                data = (
#                    '{'
#                    '"name": "' + name + '", '
#                    '"project_id": ' + str(self.managementProjectId) + ', '
#                    '"environment_id": ' + str(self.envId) + ', '
#                    '"json": ' + self.env + ''
#                    '}'
#                )
#            )
#
        name = 'Create Class'
        self.__createItemAndID(
            name = name,
            key = 'alias',
            url=self.cfg['semaphore']['api']['project_template'],
            data = (
                '{'
                    '"ssh_key_id": ' + str(self.noneKeyId) +  ', '
                    '"project_id": ' + str(self.managementProjectId) + ', '
                    '"inventory_id": ' + str(self.localhostInvId) + ', '
                    '"repository_id": ' + str(self.repositoryId) + ', '
                    '"environment_id": ' + str(self.envId) + ', '
                    '"alias": "' + name + '", '
                    '"playbook": "' + self.cfg['content_repo']['playbooks']['createClass'] + '", '
                    '"arguments": "[\\"-e\\", \\"class=##### classSize=##\\"]", '
                    '"override_args": false}'
                '}'
            )
        )

        name = 'Destroy Class'
        self.__createItemAndID(
            name = name,
            key = 'alias',
            url=self.cfg['semaphore']['api']['project_template'],
            data = (
                '{'
                    '"ssh_key_id": ' + str(self.noneKeyId) +  ', '
                    '"project_id": ' + str(self.managementProjectId) + ', '
                    '"inventory_id": ' + str(self.localhostInvId) + ', '
                    '"repository_id": ' + str(self.repositoryId) + ', '
                    '"environment_id": ' + str(self.envId) + ', '
                    '"alias": "' + name + '", '
                    '"playbook": "' + self.cfg['content_repo']['playbooks']['destroyClass'] + '", '
                    '"arguments": "[\\"-e\\", \\"class=#####\\"]", '
                    '"override_args": false}'
                '}'
            )
        )

        name = 'Build ISOs'
        self.__createItemAndID(
            name = name,
            key = 'alias',
            url=self.cfg['semaphore']['api']['project_template'],
            data = (
                '{'
                    '"ssh_key_id": ' + str(self.noneKeyId) +  ', '
                    '"project_id": ' + str(self.managementProjectId) + ', '
                    '"inventory_id": ' + str(self.controlInvId) + ', '
                    '"repository_id": ' + str(self.repositoryId) + ', '
                    '"environment_id": ' + str(self.envId) + ', '
                    '"alias": "' + name + '", '
                    '"playbook": "' + self.cfg['content_repo']['playbooks']['buildISOs'] + '", '
                    '"arguments": "[]", '
                    '"override_args": false}'
                '}'
            )
        )

        name = 'Build VMs'
        self.__createItemAndID(
            name = name,
            key = 'alias',
            url=self.cfg['semaphore']['api']['project_template'],
            data = (
                '{'
                    '"ssh_key_id": ' + str(self.noneKeyId) +  ', '
                    '"project_id": ' + str(self.managementProjectId) + ', '
                    '"inventory_id": ' + str(self.controlInvId) + ', '
                    '"repository_id": ' + str(self.repositoryId) + ', '
                    '"environment_id": ' + str(self.envId) + ', '
                    '"alias": "' + name + '", '
                    '"playbook": "' + self.cfg['content_repo']['playbooks']['buildVMs'] + '", '
                    '"arguments": "[]", '
                    '"override_args": false}'
                '}'
            )
        )

        name = 'Get VM Info'
        self.__createItemAndID(
            name = name,
            key = 'alias',
            url=self.cfg['semaphore']['api']['project_template'],
            data = (
                '{'
                    '"ssh_key_id": ' + str(self.noneKeyId) +  ', '
                    '"project_id": ' + str(self.managementProjectId) + ', '
                    '"inventory_id": ' + str(self.vCenterInvId) + ', '
                    '"repository_id": ' + str(self.repositoryId) + ', '
                    '"environment_id": ' + str(self.envId) + ', '
                    '"alias": "' + name + '", '
                    '"playbook": "' + self.cfg['content_repo']['playbooks']['getVmInfo'] + '", '
                    '"arguments": "[]", '
                    '"override_args": false}'
                '}'
            )
        )

        # This private key is used by the rous/setupNewClass.py
        #   when accessing control via Ansible
        check_output(
            [
                'sudo', 'cp',
                self.cfg['semaphore']['private_key'],
                self.cfg['semaphore']['data_dir']
            ]
        )


    def __getAccessKey(self):
        out = self.docker.dexec(
            'semaphore',
            [
                '/bin/sh', '-c',
                '""grep access_key /etc/semaphore/config.json""'
            ]
        )

        key = out.split('"')[3]
        print('Key: ' + key)

    # Helper function that checks to see if there is an
    #   item based on it's name and if there is not,
    #   it creates the item from the provided data and
    #   returns the ID
    def __createItemAndID(self, url, name, data, key='name'):
        # Debug msg
        #print('---Checking for: ' + name)
        id = self.api.getIDFromName(
            url=url,
            key=key, name=name
        )

        if id == None:
            # Debug msg
            #print('---Creating: ' + name)
            r = self.api.post(url, data)

            # Debug msg
            #pprint.pprint(vars(r))

            if r.content == b'':
                # If the ID was not returned, we
                #   have to get it again
                if id == None:
                    id = self.api.getIDFromName(
                        url=url,
                        key=key, name=name
                    )
            else:
                id = json.loads(r.text)['id']

        # Turn on with debug option
        #print('---' + name + ' ID: ' + str(id))

        return id

    def __updateApiUrlsManagementId(self):
        for key, url in self.cfg['semaphore']['api'].items():
            self.cfg['semaphore']['api'][key] = url.replace(
                '#', str(self.managementProjectId)
            )


class SemaphoreTaskArgumentError(Exception):
    """Raised when a Semaphore task could not be executed using the given arguments"""
    pass
