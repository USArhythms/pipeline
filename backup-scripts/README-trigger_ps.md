# **Pipeline processing supplemental - Remote launch script for post-acquisition processing**

trigger.ps1 is a Powershell script that calls remote script on server [where post-acquisition processing will occur]

On acquisition computer, ensure SSH is installed with pre-requisites:

On Windows 8.1 and above ssh should be installed be default however you may need to install ssh on Windows 7.

App Download & Instructions: https://github.com/PowerShell/Win32-OpenSSH/releases

User will need to modify the following variables in trigger.ps1:

**host='obis.dk.ucsd.edu'**

**user='afassihizakeri'**

Edit line (below) to run bash script on remote host:

**$remote_submission_script_full_path = '~/post_acquire.sh'**

Example above will run bash script located in user's home directory called 'post_acquire.sh'

Note: host should be server with storage directory mounted
N.B. post_acquire.sh may be configured to run Matlab, python, Julia or other on compute server

if you have problems, contact local administrator for help