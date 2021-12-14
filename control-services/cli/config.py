import json
import pprint
import subprocess
import glob
import os

class Config():
    def __init__(self, jsonConfigFile, envPath):
        
        if os.getuid() == 0:     
            print("Please do not run with sudo") 
            exit()        

        with open(jsonConfigFile) as f:
            __configs = json.load(f)

        cfg = {}

        ### Repos

        # name, org_or_user, rel_data_dir
        cfg['vater_repo'] = __configs['repos'][0]['vater_repo']
        cfg['vater_repo']['rel_image_path'] = 'control-services/images/'

        # name, org_or_user, terraform_dir, playbook_dir, vms_dir
        cfg['content_repo'] = __configs['repos'][0]['content_repo']
        cfg['content_repo']['vCenter_inventory_path'] =                                     \
            cfg['content_repo']['playbook_dir'] + '/vm.vmware.yml'

        cfg['content_repo']['playbooks'] = {}
        cfg['content_repo']['playbooks']['createClass'] =                                   \
            cfg['content_repo']['playbook_dir'] + '/createClass.yml'

        cfg['content_repo']['playbooks']['buildISOs'] =                                     \
            cfg['content_repo']['playbook_dir'] + '/buildISOs.yml'

        cfg['content_repo']['playbooks']['buildVMs'] =                                      \
            cfg['content_repo']['playbook_dir'] + '/buildVMs.yml'

        cfg['content_repo']['playbooks']['getVmInfo'] =                                     \
            cfg['content_repo']['playbook_dir'] + '/get.vm.info.yml'

        ### Host variables

        # hostname, project_path
        cfg['host'] = __configs['host']

        ps = subprocess.Popen(('hostname', '-I'), stdout=subprocess.PIPE)
        output = subprocess.check_output(('cut', '-d', ' ', '-f1'), stdin=ps.stdout)
        cfg['host']['ip'] = (output.decode('utf-8').strip())

        cfg['host']['content_dir_path'] =                                                   \
            cfg['host']['project_path'] + cfg['content_repo']['name'] + '/'

        cfg['host']['vater_dir_path'] =                                                     \
            cfg['host']['project_path'] + cfg['vater_repo']['name'] + '/'

        cfg['host']['content_git_dir_path'] =                                               \
            cfg['host']['content_dir_path'] + '.git/'

        cfg['host']['terraform_path'] =                                                     \
            cfg['host']['content_dir_path'] + cfg['content_repo']['terraform_dir'] + '/'

        cfg['host']['vms_path'] =                                                           \
            cfg['host']['content_dir_path'] + cfg['content_repo']['vms_dir'] + '/'

        ### Development variables

        # enable
        cfg['dev'] = __configs['dev']

        if cfg['dev']['enable'] == True:
            cfg['dev']['ssh_path'] =                                                        \
                cfg['host']['project_path'] + '.ssh/' 

            cfg['dev']['ssh_auth_key_path'] =                                               \
                cfg['dev']['ssh_path'] + 'authorized_keys'

            cfg['dev']['vater_key_path'] =                                                  \
                cfg['dev']['ssh_path'] + cfg['vater_repo']['name']

            cfg['dev']['content_key_path'] =                                                \
                cfg['dev']['ssh_path'] + cfg['content_repo']['name']

        ### Services

        cfg["service_list"] = []

        for service in __configs['services'][0]:
            cfg["service_list"].append(service)

        # Gitea
        # password, user, email, org_or_user, port
        cfg['gitea'] = __configs['services'][0]['gitea']


        cfg['gitea']['url'] =                                                               \
            'http://' + cfg['host']['ip'] + ':' + cfg['gitea']['port'] + '/'

        cfg['gitea']['api_url'] =                                                           \
            cfg['gitea']['url'] + 'api/v1/'

        cfg['gitea']['data_dir'] =                                                          \
            cfg['host']['project_path'] + cfg['vater_repo']['name'] + '/' +                 \
            cfg['vater_repo']['rel_data_dir'] + 'gitea/'                                    \

        cfg['gitea']['related_data_dirs'] =                                                 \
            glob.glob(cfg['gitea']['data_dir'][:-1] + '*')

        cfg['gitea']['content_repo_path'] =                                                 \
            cfg['gitea']['data_dir'] + 'git/' + cfg['content_repo']['name']

        cfg['gitea']['content_repo_git_dir_path'] =                                         \
            cfg['gitea']['content_repo_path'] + '/.git/'

        cfg['gitea']['container_content_repo'] =                                            \
            '/data/git/' + cfg['content_repo']['name']

        cfg['gitea']['config_repo_url'] =                                                   \
            cfg['gitea']['url'] + cfg['gitea']['org_or_user'] + '/' +                       \
            cfg['content_repo']['name']

        cfg['gitea']['api'] = {}
        cfg['gitea']['api']['mirror_sync_url'] =                                            \
            cfg['gitea']['api_url'] + 'repos/' + cfg['gitea']['org_or_user'] + '/' +        \
            cfg['content_repo']['name'] + '/mirror-sync'

        cfg['gitea']['api']['tokens'] =                                                     \
            cfg['gitea']['api_url'] +                                                       \
            'users/' + cfg['gitea']['user'] + '/tokens'

        cfg['gitea']['api']['orgs'] =                                                       \
            cfg['gitea']['api_url'] + 'orgs'

        cfg['gitea']['api']['content_repo'] =                                               \
            cfg['gitea']['api_url'] + 'repos/' + cfg['gitea']['org_or_user'] + '/' +        \
            cfg['content_repo']['name']

        cfg['gitea']['api']['repos_migrate'] =                                              \
            cfg['gitea']['api_url'] + 'repos/migrate'

        # Gitea Database

        # password, user, port
        cfg['gitea_db'] = __configs['services'][0]['gitea_db']

        ### Jenkins
        cfg['jenkins'] = __configs['services'][0]['jenkins']

        cfg['jenkins']['image_dir_path'] =                                                  \
            cfg['host']['vater_dir_path'] + cfg['vater_repo']['rel_image_path'] +           \
            'jenkins/'

        cfg['jenkins']['casc_file_path'] = cfg['jenkins']['image_dir_path'] + 'casc.yaml'   \

        cfg['jenkins']['casc'] = {}
        cfg['jenkins']['casc']['unclassified'] = {}
        cfg['jenkins']['casc']['unclassified']['location'] = {}
        cfg['jenkins']['casc']['unclassified']['location']['url'] = {}
        cfg['jenkins']['casc']['unclassified']['location']['url'] =                                         \
            'http://' + cfg['host']['ip'] + '/' + cfg['jenkins']['port'] + '/'

        ### Semaphore

        # password, port, user
        cfg['semaphore'] = __configs['services'][0]['semaphore']

        cfg['semaphore']['url'] =                                                           \
            'http://' + cfg['host']['ip'] + ':' + cfg['semaphore']['port'] + '/'

        cfg['semaphore']['api_url'] =                                                       \
            cfg['semaphore']['url'] + 'api/'

        cfg['semaphore']['data_dir'] =                                                      \
            cfg['host']['vater_dir_path'] + cfg['vater_repo']['rel_data_dir'] +             \
            'semaphore/'

        cfg['semaphore']['related_data_dirs'] =                                             \
            glob.glob(cfg['semaphore']['data_dir'][:-1] + '*')

        # Many of the APIs have IDs in the middle, so we insert a '#' once in the
        #   URL to represent the project ID
        cfg['semaphore']['api'] = {}
        cfg['semaphore']['api']['login'] =                                                  \
            cfg['semaphore']['api_url'] + 'auth/login'

        cfg['semaphore']['api']['tokens'] =                                                 \
            cfg['semaphore']['api_url'] + 'user/tokens'

        cfg['semaphore']['api']['projects'] =                                               \
            cfg['semaphore']['api_url'] + 'projects'

        cfg['semaphore']['api']['project_keys'] =                                           \
            cfg['semaphore']['api_url'] + 'project/#/keys'
       
        cfg['semaphore']['api']['project_repos'] =                                          \
            cfg['semaphore']['api_url'] + 'project/#/repositories'

        cfg['semaphore']['api']['project_inventory'] =                                      \
            cfg['semaphore']['api_url'] + 'project/#/inventory'

        cfg['semaphore']['api']['project_environment'] =                                    \
            cfg['semaphore']['api_url'] + 'project/#/environment'

        cfg['semaphore']['api']['project_template'] =                                       \
            cfg['semaphore']['api_url'] + 'project/#/templates'

        cfg['semaphore']['private_key'] =                                                   \
            cfg['dev']['ssh_path'] + 'semaphore'

        # Semaphore Database

        # db_password, db_user, port
        cfg['semaphore_db'] = __configs['services'][0]['semaphore_db']

        # Docker variables
        cfg['docker'] = {}

        cfg['docker']['compose_file_path'] =                                                \
            cfg['host']['vater_dir_path'] + 'control-services/docker-compose.yml'            

        cfg['docker']['env_path'] = envPath

        cfg['docker']['env'] = []

        cfg['docker']['env'].append(
            'gitea_db_user=' + cfg['gitea_db']['user']
        )

        cfg['docker']['env'].append(
            'gitea_db_password=' + cfg['gitea_db']['password']
        )

        cfg['docker']['env'].append(
            'semaphore_admin_password=' + cfg['semaphore']['password']
        )
        

        with open(envPath, 'w') as f:
            for var in cfg['docker']['env']:
                f.writelines(var + '\n') 

        self.cfg = cfg

    def __str__(self):
        return json.dumps(self.cfg, indent=4)
