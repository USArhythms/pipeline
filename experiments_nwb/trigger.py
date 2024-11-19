import paramiko
import socket

compute_host='obis.dk.ucsd.edu'
user='afassihizakeri'

# Path to the script on the remote server (default is home directory of user)
remote_submission_script_full_path = '~/post_acquire.sh'

#####################################
#AUTOMATIC COLLECTION OF SUBMISSION HOST INFO
acquisition_host_name = socket.gethostname()
acquisition_host_ip_address = socket.gethostbyname(acquisition_host_name)
#####################################

# Create an SSH client
ssh = paramiko.SSHClient()
# Automatically add the remote server's SSH key
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the remote server
ssh.connect(hostname=compute_host, username=user)

# Full remote script with arguments (quotes added in case acquisition host name has spaces)
command = f"bash {remote_submission_script_full_path} --host '{acquisition_host_name}' --ip {acquisition_host_ip_address}"
channel = ssh.get_transport().open_session()
channel.exec_command(command)

# Print the stdout, stderr of the script
std_out = channel.recv(1024).decode('utf-8')
std_err = channel.recv_stderr(1024).decode('utf-8')
print(std_out, std_err, sep='\n')

# Close the connection
ssh.close()