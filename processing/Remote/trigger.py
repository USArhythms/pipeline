"""
Trigger Remote Data Processing Script

This script triggers post-acquisition data processing on a remote compute server.
It sends the local acquisition machine's hostname and IP address to the remote server,
which uses this information to locate and process the data.

Usage:
    python trigger.py [--host HOSTNAME] [--user USERNAME] [--script SCRIPT_PATH]

Arguments:
    --host: Remote compute server hostname (default: obis.dk.ucsd.edu or COMPUTE_HOST env var)
    --user: Username for SSH connection (default: afassihizakeri or COMPUTE_USER env var)
    --script: Path to the remote script (default: ~/post_acquire.sh or REMOTE_SCRIPT env var)

Environment Variables:
    COMPUTE_HOST: Alternative way to specify the remote host
    COMPUTE_USER: Alternative way to specify the remote user
    REMOTE_SCRIPT: Alternative way to specify the remote script path

Requirements:
    - paramiko: SSH client library for Python
    - Network connectivity to the remote server
    - SSH authorization (password or key-based)
"""

import paramiko
import socket
import argparse
import sys
import os

# Default values
DEFAULT_COMPUTE_HOST = 'obis.dk.ucsd.edu'
DEFAULT_USER = 'afassihizakeri'
DEFAULT_REMOTE_SCRIPT = '~/post_acquire.sh'

def get_args():
    """Parse command line arguments or use environment variables"""
    parser = argparse.ArgumentParser(description='Trigger post-acquisition processing on a remote server.')
    parser.add_argument('--host', default=os.environ.get('COMPUTE_HOST', DEFAULT_COMPUTE_HOST),
                        help='Remote compute host (default: env COMPUTE_HOST or obis.dk.ucsd.edu)')
    parser.add_argument('--user', default=os.environ.get('COMPUTE_USER', DEFAULT_USER),
                        help='Username for remote host (default: env COMPUTE_USER or afassihizakeri)')
    parser.add_argument('--script', default=os.environ.get('REMOTE_SCRIPT', DEFAULT_REMOTE_SCRIPT),
                        help='Path to the script on remote host (default: env REMOTE_SCRIPT or ~/post_acquire.sh)')
    
    # Only parse args if called directly (not when imported for testing)
    if len(sys.argv) > 0 and sys.argv[0].endswith('trigger.py'):
        return parser.parse_args()
    else:
        # Return default values when imported
        return parser.parse_args([])

def run_trigger(compute_host, user, remote_script):
    """
    Execute the remote trigger script on the compute host
    
    This function:
    1. Determines the local acquisition machine's hostname and IP address
    2. Establishes an SSH connection to the remote compute server
    3. Executes the remote script with the local machine's information as arguments
    4. Retrieves and returns any output from the remote script
    
    Args:
        compute_host (str): The hostname of the compute server
        user (str): The username for SSH connection
        remote_script (str): Path to the remote script to execute
        
    Returns:
        tuple: (stdout, stderr) from the remote command execution
    
    Raises:
        paramiko.SSHException: If SSH connection fails
        socket.error: If hostname resolution fails
    """
    # Automatically collect submission host info
    acquisition_host_name = socket.gethostname()
    acquisition_host_ip_address = socket.gethostbyname(acquisition_host_name)
    
    # Create an SSH client
    ssh = paramiko.SSHClient()
    # Automatically add the remote server's SSH key
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Connect to the remote server
        ssh.connect(hostname=compute_host, username=user)
        
        # Full remote script with arguments (quotes added in case acquisition host name has spaces)
        command = f"bash {remote_script} --host '{acquisition_host_name}' --ip {acquisition_host_ip_address}"
        channel = ssh.get_transport().open_session()
        channel.exec_command(command)
        
        # Get the stdout, stderr of the script
        std_out = channel.recv(1024).decode('utf-8')
        std_err = channel.recv_stderr(1024).decode('utf-8')
        
        return std_out, std_err
    finally:
        # Close the connection
        ssh.close()

def main():
    """Main entry point when script is executed directly"""
    args = get_args()
    std_out, std_err = run_trigger(args.host, args.user, args.script)
    print(std_out, std_err, sep='\n')

# Only run main() if this script is executed directly (not imported)
if __name__ == "__main__":
    main()