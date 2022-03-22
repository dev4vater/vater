# VMware vSphere
==================

Packer
~~~~~~~

Convert Methodology
^^^^^^^^^^^^^^^^^^^

New Development:

- Build out the VM to understand all of the build details
- Find the method of automated installation supported by the Operating System: 
- This can vary from a specific boot command, a preseed.cfg, cloud-init with user-data and meta-data, a ks.cfg, or a windows answer file autounattend.xml

Converting Legacy:
^^^^^^^^^^^^^^^^^^

Build out the VM once to understand the installation specific questions. Research to find where the files holding that installation information might be. Identify all installed programs, files, and user accounts:

1) Base Templates
2) Specify Configuration - Specifications can be added in two main areas: 

    - the automated installation steps via edits to the related files 
    - during the provisioning steps by adding the desired provisioners and related files 
    
Best Practices
^^^^^^^^^^^^^^

- Build or use prebuilt generic builders specifically for your virtualization environment
- Verify the generic template builds properly and then use that as a base to start the specific configuration of the golden template
- When using provisioners, read the recommended use in the packer documentation to understand whether that provisioner will meet your needs
- Provisioners that accept inline commands (Shell, Powershell, etc) can accept long "one-liner" commands, but troubleshooting the build is substantially easier when commands are broken into the smallest possible strings i.e. `inline = ["one action", "another one", "etc"]`
- The `file` provisioner should be used to transfer specific files to exact file locations if the files being transferred will be used later in the packer provisioning process. Otherwise, the file provisioner will move entire directories without issue for access once the template is complete and you have your packer build artifact
- Testing provisioning builds can be the longest process in development - to save time, test the commands and scripts in a 

Tips & Tricks
^^^^^^^^^^^^^

- If no generic packer build exists for your specific operating system and environment, look for a different packer build for your desired operating system - you can then edit the builder based on the desired environment. If this is not available, find related operating systems and use them as a reference to build the generic for your system.
- Use TMUX when developing to allow better management of your build sessions. Build times range from 10 minutes to hours, so being able to keep an eye on the build progress and watch for errors while continuing other work is extremely helpful
- Having a package manager makes provisioning software installations much easier and increases code readability - most *nix flavors have one - for windows, chocolatey is a great option and it's also easy to build a chocolatey package for software you might want that isn't supported already
