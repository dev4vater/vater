.. image::  https://github.com/dev4vater/vater/blob/readthedocs_setup/diagram/MADDUCK.JPG
   :width: 400

Project goal
------------

VATER == Virtualization-Agnostic Training and Evaluation Range

The goal of VATER is to develop an interactive range that can be
utilized by students, with a focus on making the range solution
resilient and sustainable in the face of anticipated changes. This range
will be created using Infrastructure As Code (IAC) principles.

Infrastructure As Code
----------------------

Infrastructure As Code is the managing and provisioning of
infrastructure through code, either with scripts or declarative
definitions, instead of through manual processes.

Some benefits of implementing with IAC design principles include:

-  **Infrastructure automation:** IAC enables speed through faster
   execution when configuring the infrastructure and removes the risk
   associated with human error, like manual configuration.

-  **Range content maintenance:** Instructors and range scenario
   developers make changes in one centralized location in a way that
   removes any ambiguity or need for interpretation on the part of those
   who inherit the range years down the road.

-  **Consistent student experience:** By documenting your configuration
   specification, IAC aids configuration management and helps avoid
   undocumented, ad-hoc configuration changes. As a result, students
   will have the same environment every time.

Key VATER Components
--------------------

With IAC, the IT infrastructure managed includes physical equipment,
such as bare-metal servers, virtual machines, and associated
configuration resources.

-  **Ansible:** can be used to describe the desired state of the
   infrastructure, which the tool can then provision. Ansible Automation
   can also be used for configuration management to maintain the systems
   in the desired state.

-  **Gitea:** is an open-source software package for hosting software
   development version control using Git as well as other collaborative
   features like bug tracking, wikis, and code review.

-  **Packer:** is an IAC tool that enables the developer to define a
   virtual machine purely in a code-based configuration file. This
   provides an alternative to the traditional model of building and
   maintaining virtual machine snapshots.

-  **Terraform:** is an IAC tool that allows the user to build, change,
   and version infrastructure safely and efficiently. Terraform uses a
   high-level configuration language in human-readable, declarative
   configuration files.

-  **Guacamole:** is a clientless remote desktop gateway that supports
   standard protocols like VNC, RDP, and SSH. As long as you have access
   to a web browser, you have access to your machines.

.. image:: https://github.com/uwardlaw/vater/blob/main/diagram/range.svg
   :width: 400

VATER Interface for Instructors
-------------------------------

.. image:: https://github.com/uwardlaw/vater/blob/main/diagram/instructorExperience.svg
   :width: 400
