<#
.SYNOPSIS
Triggers post-acquisition data processing on a remote compute server.

.DESCRIPTION
This PowerShell script connects to a remote compute server via SSH and triggers 
post-acquisition data processing by executing a remote script. It automatically 
collects and passes the local hostname and IP address to the remote server.

.PARAMETER ComputeHost
The remote compute server hostname. Default is 'obis.dk.ucsd.edu' or value from COMPUTE_HOST environment variable.

.PARAMETER User
Username for SSH connection. Default is 'afassihizakeri' or value from COMPUTE_USER environment variable.

.PARAMETER RemoteScript
Path to the script on the remote server. Default is '~/post_acquire.sh' or value from REMOTE_SCRIPT environment variable.

.EXAMPLE
.\trigger.ps1
# Uses default parameters

.EXAMPLE
.\trigger.ps1 -ComputeHost "myserver.example.com" -User "username" -RemoteScript "~/myscript.sh"
# Uses custom server, username, and script path

.NOTES
Version: 2.0
Requires: PowerShell 5.0 or later
SSH must be installed and configured for the Windows system
#>

# Define parameters with defaults
param(
    [string]$ComputeHost = $(if ($env:COMPUTE_HOST) { $env:COMPUTE_HOST } else { 'obis.dk.ucsd.edu' }),
    [string]$User = $(if ($env:COMPUTE_USER) { $env:COMPUTE_USER } else { 'afassihizakeri' }),
    [string]$RemoteScript = $(if ($env:REMOTE_SCRIPT) { $env:REMOTE_SCRIPT } else { '~/post_acquire.sh' })
)

# Function to collect acquisition host information
function Get-AcquisitionHostInfo {
    [CmdletBinding()]
    param()
    
    try {
        $hostName = [System.Net.Dns]::GetHostName()
        $ipAddress = [System.Net.Dns]::GetHostAddresses($hostName) | 
                     Where-Object { $_.AddressFamily -eq 'InterNetwork' } | 
                     Select-Object -First 1
                     
        if ($null -eq $ipAddress) {
            Write-Error "Unable to determine local IP address"
            return $null
        }
        
        $ipAddressString = $ipAddress.IPAddressToString
        
        return @{
            HostName = $hostName
            IPAddress = $ipAddressString
        }
    }
    catch {
        Write-Error "Error collecting host information: $_"
        return $null
    }
}

# Function to execute the remote trigger via SSH
function Invoke-RemoteTrigger {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$ComputeHost,
        
        [Parameter(Mandatory=$true)]
        [string]$User,
        
        [Parameter(Mandatory=$true)]
        [string]$RemoteScript,
        
        [Parameter(Mandatory=$true)]
        [string]$LocalHostName,
        
        [Parameter(Mandatory=$true)]
        [string]$LocalIPAddress
    )
    
    try {
        $sshCommand = "ssh -o StrictHostKeyChecking=no $User@$ComputeHost 'bash $RemoteScript --host $LocalHostName --ip $LocalIPAddress'"
        
        Write-Verbose "Executing command: $sshCommand"
        $result = Invoke-Expression $sshCommand
        
        return @{
            Success = $true
            Output = $result
        }
    }
    catch {
        Write-Error "Error executing SSH command: $_"
        return @{
            Success = $false
            Error = $_.Exception.Message
        }
    }
}

# Main execution - only run if script is not being dot-sourced (imported)
if ($MyInvocation.InvocationName -ne ".") {
    # Get acquisition host information
    $hostInfo = Get-AcquisitionHostInfo
    
    if ($null -eq $hostInfo) {
        Write-Error "Failed to get acquisition host information. Exiting."
        exit 1
    }
    
    # Execute the remote trigger
    $result = Invoke-RemoteTrigger -ComputeHost $ComputeHost -User $User -RemoteScript $RemoteScript `
                                  -LocalHostName $hostInfo.HostName -LocalIPAddress $hostInfo.IPAddress `
                                  -Verbose:$VerbosePreference
    
    if ($result.Success) {
        Write-Output "Remote trigger executed successfully"
        if ($result.Output) {
            Write-Output "Output: $($result.Output)"
        }
        exit 0
    }
    else {
        Write-Error "Remote trigger failed: $($result.Error)"
        exit 1
    }
}