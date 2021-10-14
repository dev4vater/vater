# Control

Control exposes a frontend for developers, students, and instructors to interact with the lab environment. 

- Gitea is a web GUI for git
- Semaphore is web GUI for Ansible
- Guacamole is a clientless remote administration gateway

## Structure
```
.
|-- README.md
|-- bin                                # Holds scripts used to manage host VM and containers
|   |-- accessContainer.sh               # Convenience script for getting a shell from some containers
|   |-- clean.sh                         # Cleans all artifacts, including data-- execute bit off by default
|   |-- createSemaphoreManagement.py     # Used by restart.sh to configure Semaphore, idempotent
|   |-- restart.sh                       # Prepares folders and configurations for containers and starts them, idempotent
|   |-- setup.sh                         # Run once when the host VM is first installed
|   `-- stop.sh                          # Stops all containers and cleans hanging artificats 
|-- data                               # Persistent data for the containers
|   |-- gitea 
|   |-- gitea_db
|   |-- guac_db
|   |-- guacd
|   |-- semaphore
|   `-- semaphore_db
|-- docker-compose.yml                # Manages relationships between multiple containers
`-- images                            # Holds instructions to build modified images
    `-- semaphore
```

## Day 0 Installation

TODO

## Resources
 
### Ansible
[Deploy VM from template](https://docs.ansible.com/ansible/latest/scenario_guides/vmware_scenarios/scenario_clone_template.html)
[Playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html)
[AWK Playbooks for vCenter](https://www.robvit.com/ansible-tower-awx/ansible-vmware-playbook-examples/)
[Playbook Keywords](https://docs.ansible.com/ansible/latest/reference_appendices/playbooks_keywords.html)
[Dynammic vCenter inventory](http://vcloud-lab.com/entries/devops/ansible-for-vmwary-using-vmware-vm-inventory-dynamic-inventory-plugin)
[Implicit localhost](https://docs.ansible.com/ansible/2.6/inventory/implicit_localhost.html)
[vCenter guide](https://pelegit.co.il/how-to-run-ansible-on-vcenter/)
[Primary Ansible reference for VMware](https://docs.ansible.com/ansible/latest/collections/community/vmware/index.html#scenario-guide)

### Containers
[Root user in Semaphore](https://stackoverflow.com/questions/61683448/how-to-run-bash-as-user-root-on-alpine-images-with-docker-su-must-be-suid-to-w)

#B## Gitea

### Semaphore
[Semaphore dockerfile](https://github.com/ansible-semaphore/semaphore/blob/develop/deployment/docker/dev/Dockerfile)

