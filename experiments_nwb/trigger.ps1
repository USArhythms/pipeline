# trigger.ps1
# Version 1.0

#REMOTE PROCEDURE CALL TO BE RUN ON ACQUISITION COMPUTER (WINDOWS)

$compute_host = 'obis.dk.ucsd.edu'
$user = 'afassihizakeri'

# Path to the script on the remote server (default is home directory of user)
$remote_submission_script_full_path = '~/post_acquire.sh'

#####################################
#AUTOMATIC COLLECTION OF SUBMISSION HOST INFO
$acquisition_host_name = [System.Net.Dns]::GetHostName()
$acquisition_host_ip_address = [System.Net.Dns]::GetHostAddresses($acquisition_host_name) | Where-Object { $_.AddressFamily -eq 'InterNetwork' } | Select-Object -First 1
$acquisition_host_ip_address_string = $acquisition_host_ip_address.IPAddressToString
#####################################

$ssh_command = "ssh -o StrictHostKeyChecking=no $user@$compute_host 'bash $remote_submission_script_full_path --host $acquisition_host_name --ip $acquisition_host_ip_address_string'"

# Execute the SSH command
Invoke-Expression $ssh_command