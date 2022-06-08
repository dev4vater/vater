# Full Documentation: https://mad-ducks-vater.readthedocs.io

## Structure

```
.
├── control-services
│   ├── bin                             # Utility scripts not for direct Vater service interaction
│   │   └── setup.sh
│   ├── cli                             # A command line interface for working with Vater services
│   │   ├── api.py
│   │   ├── config.py
│   │   ├── dev.py
│   │   ├── gitea.py
│   │   ├── __init__.py
│   │   ├── parser.py
│   │   ├── __pycache__
│   │   ├── semaphore.py
│   │   ├── vater.py
│   │   └── vDocker.py
│   ├── config.json                     # A configuration file for changing Vater settings
│   ├── data                            # Persistent service data
│   │   ├── gitea
│   │   ├── gitea_db
│   │   ├── semaphore
│   │   └── semaphore_db
│   ├── docker-compose.yml              # Instructions for configuring the service containers
│   ├── images                          # Augmented service images
│   │   └── semaphore
│   └── README.md
├── diagram                             # Diagrams for the Wiki
│   ├── instructorExperience.drawio
│   ├── instructorExperience.svg
│   ├── MADDUCK.JPG
│   ├── range.drawio
│   ├── range.svg
│   ├── terraformDesign.drawio
│   ├── terraformDesign.svg
│   └── vaterCLI.drawio
└── README.md
```

## Day 0 Deployment
- **Manually** provision `Control` VM
  - The user and hostname need to be `Control` or you need to edit the `config.json`
  - `Ubuntu 20.04`
    - 2 vCPUS
    - 4 GB RAM
    - 60 GB storage in `/`
- **Manually** git clone `https://github.com/dev4vater/vater` into `~`
- **Manually** run ` ~/vater/control-services/bin/setup.sh`
- `setup.sh` will create a RSA key pair if one does not exist and print the public key to the terminal
- **Manually** copy the public RSA key
- **Manually** input public RSA key into `github` settings ssh key
- `setup.sh` will pull `marissaeinhorn/rous` locally
- **Manually** run `vater restart`
- When prompted to enter the `gitea` and `semaphore` passwords wait 2 min before entering password to ensure database is fully initialized
