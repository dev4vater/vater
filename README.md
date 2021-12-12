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
│   │   ├── guacd
│   │   ├── guac_db
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
- **Manually** git clone `https://github.com/uwardlaw/vater` into `~`
- **Manually** run ` ~/vater/control-services/bin/setup.sh`
- `setup.sh` will create a RSA key pair if one does not exist and print the public key to the terminal
- **Manually** copy the public RSA key
- **Manually** input public RSA key into `uwardlaw/rous` as a deploy key 
- `setup.sh` will pull `uwardlaw/rous` locally
- **Manually** run `vater restart`

(Developed in Nano)
