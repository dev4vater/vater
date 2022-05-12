Launch - Replacing Day 0 Deployment
===================================

Objectives
----------

-  standard environment
-  cross platform

   -  currently ``.ps1`` & ``.sh`` for ``Windows`` and ``*nix``
      respectively
   -  could look at using ``python3``

-  two main deployment schemes: Enterprise vs Home

Enterprise Deployment - Launch for ``vSphere``
----------------------------------------------

Not in progress
~~~~~~~~~~~~~~~

1) Dependencies

   -  Specific version numbers

2) Build Control
3) Configure Control

   -  Using ``control.py``

Home Deployment - Launch for ``VirtualBox``
-------------------------------------------

Current Progress
~~~~~~~~~~~~~~~~

1) Get ``Vbox`` 

   - Install ``Chocolatey`` (package manager) 
   - ``choco install vbox`` 

2) Get other dev tools

   - ``choco install nano/vim``
   - ``choco install packer`` 

3) Need Control (2 options) 

   - Build control with ``VboxManage`` (**current**)
   - Build control with packer 

4) Configure Control (2 options)

   - run ``control.py`` via ``VboxManage`` 
   - include ``control.py`` in the ``packer`` build of control with a python provisioning block
