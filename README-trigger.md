# **Pipeline processing supplemental - Remote launch script for post-acquisition processing**

THIS SCRIPT REQUIRES PREREQUISITES AND MAY INVOLVE MORE WORK THAN POWERSHELL REMOTE PROCEDURE CALL (RPC).

IN ADDITION, THE CRYPTOGRAPHY LIBRARIES MAY NOT BE INSTALLED ON WINDOWS 7 AND BELOW

trigger.py calls remote script on server [where post-acquisition processing will occur]

On acquisition computer, ensure python v3 is installed with pre-requisites:

On Powershell terminal run: 

    python -V (ensures python is installed and user will see version)

    pip show paramiko (ensures paramiko module is installed)

    Note: If paramiko is not installed, you may install with: 
    pip install paramiko

User will need to modify the following variables in trigger.py:
host='obis.dk.ucsd.edu'
user='afassihizakeri'

Edit line (below) to run python script on remote host:

**stdin, stdout, stderr = ssh.exec_command('python3 ~/process.py')**

Example above will run python script located in user's home directory called 'process.py'

Note: host should be server with storage directory mounted

if you have problems, contact local administrator for help