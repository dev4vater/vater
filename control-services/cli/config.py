import json
import pprint
import subprocess
import glob
import os
import yaml
from dotenv import find_dotenv, dotenv_values


class Config:
    def __init__(self):

        if os.getuid() == 0:
            print("Please do not run with sudo")
            exit()

        # Load environment variables
        env_path = find_dotenv(".env")
        env_vars = dotenv_values(env_path)

        cfg = {}

        ### Repos
        cfg["vater_repo"] = {
            "rel_data_dir": "control-services/data/",
            "rel_image_path": "control-services/images/",
            "name": "vater",
            "org_or_user": "dev4vater",
        }

        cfg["content_repo"] = {
            "playbook_dir": "tasks",
            "terraform_dir": "terraform",
            "vms_dir": "vms",
            "vCenter_inventory_path": "tasks/vm.vmware.yml",
            "name": "rous",
            "org_or_user": "marissaeinhorn",
            "playbooks": {
                "createClass": "tasks/createClass.yml",
                "destroyClass": "tasks/destroyClass.yml",
                "buildISOs": "tasks/buildISOs.yml",
                "buildVMs": "tasks/buildVMs.yml",
                "getVmInfo": "tasks/get.vm.info.yml",
            },
        }

        ### Host variables
        cfg["host"] = {
            "hostname": "control",
            "project_path": "/home/control/",
            "content_dir_path": "/home/control/rous/",
            "vater_dir_path": "/home/control/vater/",
            "content_git_dir_path": "/home/control/rous/.git/",
            "terraform_path": "/home/control/rous/terraform/",
            "vms_path": "/home/control/rous/vms/",
        }

        # Get host ip
        ps = subprocess.Popen(("hostname", "-I"), stdout=subprocess.PIPE)
        output = subprocess.check_output(("cut", "-d", " ", "-f1"), stdin=ps.stdout)
        cfg["host"]["ip"] = output.decode("utf-8").strip()

        ### Development variables
        cfg["dev"] = {
            "enable": True,
            "ssh_path": "/home/control/.ssh/",
            "ssh_auth_key_path": "/home/control/.ssh/authorized_keys",
            "vater_key_path": "/home/control/.ssh/vater",
            "content_key_path": "/home/control/.ssh/rous",
        }

        ### Services
        cfg["service_list"] = [
            "gitea",
            "gitea_db",
            "semaphore",
            "semaphore_db",
            "jenkins",
        ]

        # Gitea
        # Obtain user/pass from environment var
        cfg["gitea"] = {
            "password": env_vars.get("gitea_password"),
            "user": env_vars.get("gitea_user"),
            "email": "config@example.com",
            "org_or_user": "333TRS",
            "port": env_vars.get("gitea_port"),
        }

        cfg["gitea"]["url"] = (
            "http://" + cfg["host"]["ip"] + ":" + cfg["gitea"]["port"] + "/"
        )

        cfg["gitea"]["api_url"] = cfg["gitea"]["url"] + "api/v1/"

        cfg["gitea"]["data_dir"] = (
            cfg["host"]["project_path"]
            + cfg["vater_repo"]["name"]
            + "/"
            + cfg["vater_repo"]["rel_data_dir"]
            + "gitea/"
        )

        cfg["gitea"]["related_data_dirs"] = glob.glob(
            cfg["gitea"]["data_dir"][:-1] + "*"
        )

        cfg["gitea"]["content_repo_path"] = (
            cfg["gitea"]["data_dir"] + "git/" + cfg["content_repo"]["name"]
        )

        cfg["gitea"]["content_repo_git_dir_path"] = (
            cfg["gitea"]["content_repo_path"] + "/.git/"
        )

        cfg["gitea"]["container_content_repo"] = (
            "/data/git/" + cfg["content_repo"]["name"]
        )

        cfg["gitea"]["config_repo_url"] = (
            cfg["gitea"]["url"]
            + cfg["gitea"]["org_or_user"]
            + "/"
            + cfg["content_repo"]["name"]
        )

        cfg["gitea"]["api"] = {}

        cfg["gitea"]["api"]["orgs"] = cfg["gitea"]["api_url"] + "orgs"

        cfg["gitea"]["api"]["repos_migrate"] = cfg["gitea"]["api_url"] + "repos/migrate"

        cfg["gitea"]["api"]["mirror_sync_url"] = (
            cfg["gitea"]["api_url"]
            + "repos/"
            + cfg["gitea"]["org_or_user"]
            + "/"
            + cfg["content_repo"]["name"]
            + "/mirror-sync"
        )

        cfg["gitea"]["api"]["tokens"] = (
            cfg["gitea"]["api_url"] + "users/" + cfg["gitea"]["user"] + "/tokens"
        )

        cfg["gitea"]["api"]["content_repo"] = (
            cfg["gitea"]["api_url"]
            + "repos/"
            + cfg["gitea"]["org_or_user"]
            + "/"
            + cfg["content_repo"]["name"]
        )

        ### Gitea Database
        # Obtain user/pass from environment var
        cfg["gitea_db"] = {
            "password": env_vars.get("gitea_db_password"),
            "user": env_vars.get("gitea_db_user"),
            "port": env_vars.get("gitea_db_port"),
        }

        ### Jenkins
        # Obtain user/pass from environment var
        cfg["jenkins"] = {
            "password": env_vars.get("jenkins_admin_password"),
            "user": env_vars.get("jenkins_admin_id"),
            "port": env_vars.get("jenkins_port"),
        }

        cfg["jenkins"]["image_dir_path"] = (
            cfg["host"]["vater_dir_path"]
            + cfg["vater_repo"]["rel_image_path"]
            + "jenkins/"
        )

        cfg["jenkins"]["data_dir_path"] = (
            cfg["host"]["vater_dir_path"] + "control-services/data/jenkins/"
        )

        cfg["jenkins"]["casc_file_path"] = (
            cfg["jenkins"]["image_dir_path"] + "casc.yaml"
        )

        casc_temp_str = cfg["jenkins"]["image_dir_path"] + "casc_template.yaml"
        with open(casc_temp_str, "r") as cascTemplate:
            cfg["jenkins"]["casc"] = yaml.load(cascTemplate, yaml.SafeLoader)

        cfg["jenkins"]["casc"]["unclassified"]["location"]["url"] = (
            "http://" + cfg["host"]["ip"] + ":" + cfg["jenkins"]["port"] + "/"
        )

        ### Semaphore
        # Obtain user/pass from environment var
        cfg["semaphore"] = {
            "password": env_vars.get("semaphore_admin_password"),
            "user": env_vars.get("semaphore_admin_name"),
            "port": env_vars.get("semaphore_port"),
        }

        cfg["semaphore"]["url"] = (
            "http://" + cfg["host"]["ip"] + ":" + cfg["semaphore"]["port"] + "/"
        )

        cfg["semaphore"]["api_url"] = cfg["semaphore"]["url"] + "api/"

        cfg["semaphore"]["data_dir"] = (
            cfg["host"]["vater_dir_path"]
            + cfg["vater_repo"]["rel_data_dir"]
            + "semaphore/"
        )

        cfg["semaphore"]["related_data_dirs"] = glob.glob(
            cfg["semaphore"]["data_dir"][:-1] + "*"
        )

        # Build information

        cfg["semaphore"]["build"] = {}
        cfg["semaphore"]["build"]["parent_dir"] = (
            cfg["host"]["vater_dir_path"]
            + cfg["vater_repo"]["rel_image_path"]
            + "semaphore/build/"
        )

        cfg["semaphore"]["build"]["dir"] = (
            cfg["semaphore"]["build"]["parent_dir"]
            + "src/github.com/ansible-semaphore/"
        )

        cfg["semaphore"]["build"]["source_dir"] = (
            cfg["semaphore"]["build"]["dir"] + "semaphore/"
        )

        # Many of the APIs have IDs in the middle, so we insert a '#'
        # once in the URL to represent the project ID
        cfg["semaphore"]["api"] = {}
        cfg["semaphore"]["api"]["login"] = cfg["semaphore"]["api_url"] + "auth/login"

        cfg["semaphore"]["api"]["tokens"] = cfg["semaphore"]["api_url"] + "user/tokens"

        cfg["semaphore"]["api"]["projects"] = cfg["semaphore"]["api_url"] + "projects"

        cfg["semaphore"]["api"]["project_keys"] = (
            cfg["semaphore"]["api_url"] + "project/#/keys"
        )

        cfg["semaphore"]["api"]["project_repos"] = (
            cfg["semaphore"]["api_url"] + "project/#/repositories"
        )

        cfg["semaphore"]["api"]["project_inventory"] = (
            cfg["semaphore"]["api_url"] + "project/#/inventory"
        )

        cfg["semaphore"]["api"]["project_environment"] = (
            cfg["semaphore"]["api_url"] + "project/#/environment"
        )

        cfg["semaphore"]["api"]["project_template"] = (
            cfg["semaphore"]["api_url"] + "project/#/templates"
        )

        cfg["semaphore"]["api"]["project_tasks"] = (
            cfg["semaphore"]["api_url"] + "project/#/tasks"
        )

        cfg["semaphore"]["private_key"] = cfg["dev"]["ssh_path"] + "semaphore"

        ## Semaphore Database
        # Obtain user/pass from environment var
        cfg["semaphore_db"] = {
            "password": env_vars.get("semaphore_db_password"),
            "user": env_vars.get("semaphore_db_user"),
            "port": env_vars.get("semaphore_db_port"),
        }

        ## Docker variables
        cfg["docker"] = {
            "compose_file_path": "/home/control/vater/control-services/docker-compose.yml",
            "env_path": env_path,
            "env": [],
        }

        """
        Save docker environment variables into a formatted list for vDocker.py
        to utilize in managing/interfacing with containers
        """
        for env_key in env_vars:
            cfg["docker"]["env"].append(f"{env_key}={env_vars[env_key]}")

        self.cfg = cfg

        self.setupDataFolders()

    def setupDataFolders(self):
        for service in self.cfg["service_list"]:
            dirPath = (
                self.cfg["host"]["vater_dir_path"]
                + self.cfg["vater_repo"]["rel_data_dir"]
                + service
            )

            if not os.path.exists(dirPath):
                os.makedirs(dirPath)

    def __str__(self):
        return json.dumps(self.cfg, indent=4)
