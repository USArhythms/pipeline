# **Pipeline processing supplemental - Windows to Linux password-less SSH**

    1. Open Powershell (terminal)
    2. Type: ssh-keygen -t rsa -b 2048 (select defaults - now password, files in default location '~/.ssh/')
    3. type %USERPROFILE%\.ssh\id_rsa.pub | ssh user@linux-server "cat >> ~/.ssh/authorized_keys"
    Example: %USERPROFILE%\.ssh\id_rsa.pub | ssh drinehart@obis.dk.ucsd.edu "cat >> ~/.ssh/authorized_keys"
    4. Login to remote server using SSH. No password should be required.
    
    if you have problems, contact local administrator for help