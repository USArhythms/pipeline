import paramiko

host='obis.dk.ucsd.edu'
user='afassihizakeri'

#####################################

# Create an SSH client
ssh = paramiko.SSHClient()
# Automatically add the remote server's SSH key
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the remote server
ssh.connect(hostname=host, username=user)

# Execute the remote script
#Note: post_acquire.sh is located in home directory of user defined at top of script
stdin, stdout, stderr = ssh.exec_command('bash ~/post_acquire.sh')

# Print the output of the script
print(stdout.read().decode())
print(stderr.read().decode())

# Close the connection
ssh.close()
