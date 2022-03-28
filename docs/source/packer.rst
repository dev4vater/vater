Getting Started with Packer
==========================

Packer enables developers to create identical machine images for multiple platforms from a single source template. Packer can automate the creation of any type of machine image, including Docker images. 

- **Builds** are a single task that eventually produces an image for a single platform. 

- **Provisioners** are components of Packer that install and configure software within a running machine prior to that machine being turned into a static image. They perform the major work of making the image contain useful software. 

- **Templates** are files which define one or more builds by configuring the various components of Packer. Packer is able to read a template and use that information to create multiple machine images in parallel.

More Information:

 `Installing Packer <https://learn.hashicorp.com/tutorials/packer/get-started-install-cli?in=packer/docker-get-started>`__ 

 `Terminology <https://www.packer.io/docs/terminology>`__ 

Packer and Docker
~~~~~~~~~~~~~~~~~

**Builders** are components of Packer that are able to create a machine image for a single platform. Builders read in some configuration and use that to run and generate a machine image. 

The docker Packer builder builds Docker images using Docker. The builder starts a Docker container, runs provisioners within this container, then exports the container for reuse or commits the image. Packer is able to provision containers with portable scripts or configuration management systems that are not tied to Docker in any way.

The Docker builder must run on a machine that has Docker Engine installed. The builder only works on machines that support Docker and does not support running on a Docker remote host.

More Information:

`Docker Builder <https://www.packer.io/plugins/builders/docker>`_

Packer CLI
~~~~~~~~~~

Packer is controlled using a command-line interface. **Commands** are sub-commands for the packer program that perform some job. Packer ships with a set of commands out of the box in order to define its command-line interface.

Subcommands are executed with packer SUBCOMMAND, where "SUBCOMMAND" is the actual command you wish to execute. Packer supports a fully machine-readable output setting, allowing you to use Packer in automated environments.

More Information: 

`Commands <https://www.packer.io/docs/commands>`__ 

Packer Templates
~~~~~~~~~~~~~~~~~

Packer's behavior is determined by the Packer template, which consists of a series of declarations and commands for Packer to follow. This template tells Packer what plugins (builders, provisioners, post-processors) to use, how to configure each of those plugins, and what order to run them in.

Packer is transitioning to a new template configuration format that uses HCL2 -- the same configuration language used by Terraform and HashiCorp's other products. 

More Information: 

`HCL Templates <https://www.packer.io/docs/templates/hcl_templates>`__

Packer Chaining
~~~~~~~~~~~~~~~~

**Chaining** image builds refers to breaking your provisioners out into multiple templates and chaining the builds such that the output from a prior build is the base image to configure in the subsequent build.

Benefits of chaining include a reduction in time during the image building process and image development as well as maximum maintainability of code and reuse of infrastructure code across divergent configurations. 

More Information: 

`Chaining <https://medium.com/swlh/chaining-machine-image-builds-with-packer-b6fd99e35049>`__

`Chaining in VATER <https://github.com/uwardlaw/vater/issues/130>`__

VATER Packer Repo 
~~~~~~~~~~~~~~

Generic Packer Templates with chained builders for Proxmox, Vagrant, VirtualBox, VMWare, and vSphere

`Pack_Everything <https://github.com/rylagek/pack_everything>`__

Windows
~~~~~~~

`Windows Walkthrough <https://www.danielmartins.online/post/hashicorp-packer-build-hcl-windows-10-pro-using-vmware-vsphere-iso-builder>`__

*Nix
~~~~~~~

cloud-init (ubuntu 20.04+)

- `Blog <https://beryju.org/blog/automating-ubuntu-server-20-04-with-packer>`__

- `Code <https://github.com/BeryJu/infrastructure/tree/master/packer>`__ 

kickstarter (rocky/centos) 

- `Rocky8 example <https://github.com/eaksel/packer-Rocky8>`__

Limit to Parallel Builds
~~~~~~~~~~~~~~~~~~~~~~~~

Parallel builds, while time efficient are resource intensive - current resources prevent >4 parallel builds

.. Warning:: More builds attempted will fail due to memory usage

