Packer Intro
------------

Packer Docs - `Terminology <https://www.packer.io/docs/terminology>`__ -
`Commands <https://www.packer.io/docs/commands>`__ - `HCL
Templates <https://www.packer.io/docs/templates/hcl_templates>`__

Packer Examples
---------------

`Pack_Everything <https://github.com/rylagek/pack_everything>`__ - repo
with Generic Packer Builds - **active development**

`Windows
Walkthrough <https://www.danielmartins.online/post/hashicorp-packer-build-hcl-windows-10-pro-using-vmware-vsphere-iso-builder>`__

\*Nix - preseed (ubuntu <= 18.04) - cloud-init (ubuntu 20.04+)
`Blog <https://beryju.org/blog/automating-ubuntu-server-20-04-with-packer>`__
and
`Code <https://github.com/BeryJu/infrastructure/tree/master/packer>`__ -
kickstarter (rocky/centos) `Rocky8
example <https://github.com/eaksel/packer-Rocky8>`__

Chaining -
https://medium.com/swlh/chaining-machine-image-builds-with-packer-b6fd99e35049
- https://github.com/uwardlaw/vater/issues/130

Limit to parallel builds
------------------------

Parallel builds, while time efficient are resource intensive - current
resources prevent **>4** parallel builds - more builds attempted will
fail due to memory usage
