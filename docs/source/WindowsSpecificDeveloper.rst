Windows Developer Guide
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. Note:: This Guide is to be used prior to Packer


<ComputerName>*</ComputerName>
Or
Set new computer name `Rename-computer -newname {server name}`
*Must* Restart after `Restart-Computer`

Set static IP - component Microsoft-Windows-TCPIP
Add `interface`
Set `Ipv4(6)Settings`
`UnicastIpAddress` is the static ip - set as desired
Or `New-NetIPAddress` -InterfaceIndex 4 -IPAddress 192.168.61.100 -PrefixLength 24 DefaultGateway 192.168.61.2`

Set DNS - component Miscrosoft-Windows-DNS-Client
Or
`Set-DnsClientServerAddress -InterfaceIndex 4 -ServerAddresses ("192.168.61.100","8.8.8.8")`

Scripting Server setup and management
Use AD DS configuration wizard to generate the powershell scripts needed
first: Domain controller (root)

Child DC
set root DC as DNS server `Set-DnsClientServerAddress -Interface $InterfaceNumber -ServerAddress ('xxx.xx.xx.x', ...)` where interface number is the interface you want (found via `Get-NetIPInterface`)
- this will need to happen twice: first for the development portion and then reset before templating

Scripting:
Install [windows feature](https://social.technet.microsoft.com/wiki/contents/articles/29380.install-adds-using-powershell.aspx)
Then run the above scripts
add `-SafeModeAdministratorPassword (convertto-Securestring -AsPlainText -Force asd@123)`
add `-SkipPreChecks`

View Logging:
https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/deploy/troubleshooting-domain-controller-deployment

Windows File transfers (faster than packer file provisioner)

Using ORCA to create silent installs of MSI

For simplicity - add second interface for DHCP internet access w/ dev environment and remove w/ packer ps provisioner

https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.management/new-psdrive?view=powershell-7.2
`$cred = Get-Credential -Credential Contoso\ServiceAccount New-PSDrive -Name "S" -Root "\\Server01\Scripts" -Persist -PSProvider "FileSystem" -Credential $cred -Scope Global`


Windows Scheduled tasks https://devblogs.microsoft.com/scripting/use-powershell-to-create-scheduled-tasks/
From a shared directory https://devblogs.microsoft.com/scripting/how-to-run-powershell-scripts-from-a-shared-directory/

Create Persistent Drive https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.management/new-psdrive?view=powershell-5.1

SMB Network share: https://www.msnoob.com/powershell-command-to-create-a-network-share.html

the difference: https://blog.wisefaq.com/2020/04/23/new-smbmapping-vs-new-psdrive/

linux zipping for windows compatibility: https://superuser.com/questions/5155/how-to-create-a-zip-file-compatible-with-windows-under-linux
