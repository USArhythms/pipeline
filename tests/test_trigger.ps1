<#
.SYNOPSIS
Test suite for the trigger.ps1 script

.DESCRIPTION
This PowerShell test script validates the functionality of trigger.ps1.
It uses Pester framework-like approach to test individual functions
without requiring actual SSH connections.

.NOTES
Requirements:
- PowerShell 5.0 or later
#>

# Source the script to test (dot-sourcing makes functions available in this scope)
. (Join-Path -Path $PSScriptRoot -ChildPath '..\experiments_nwb\trigger.ps1')

# Define test functions
function Test-GetAcquisitionHostInfo {
    Write-Host "Testing Get-AcquisitionHostInfo function..."
    
    $hostInfo = Get-AcquisitionHostInfo
    
    if ($null -eq $hostInfo) {
        Write-Host "FAILED: Get-AcquisitionHostInfo returned null" -ForegroundColor Red
        return $false
    }
    
    if ([string]::IsNullOrEmpty($hostInfo.HostName)) {
        Write-Host "FAILED: HostName is null or empty" -ForegroundColor Red
        return $false
    }
    
    if ([string]::IsNullOrEmpty($hostInfo.IPAddress)) {
        Write-Host "FAILED: IPAddress is null or empty" -ForegroundColor Red
        return $false
    }
    
    Write-Host "PASSED: Get-AcquisitionHostInfo returned valid host information" -ForegroundColor Green
    Write-Host "  HostName: $($hostInfo.HostName)" -ForegroundColor Gray
    Write-Host "  IPAddress: $($hostInfo.IPAddress)" -ForegroundColor Gray
    return $true
}

function Test-InvokeRemoteTriggerMock {
    Write-Host "Testing Invoke-RemoteTrigger with mocked SSH..."
      # Use a different approach to mock Invoke-Expression
    try {
        # Store the original script content to be restored later
        $originalScriptContent = Get-Content -Path (Join-Path -Path $PSScriptRoot -ChildPath '..\experiments_nwb\trigger.ps1') -Raw
        
        # Create a modified version of the script with our mock
        $mockScript = $originalScriptContent -replace 'Invoke-Expression \$sshCommand', 'if ($sshCommand -like "*ssh*" -and $sshCommand -like "*--host*" -and $sshCommand -like "*--ip*") { "Mocked SSH output - Success" } else { throw "Mock SSH command failed validation" }'
        
        # Write the modified script to a temporary file
        $tempScriptPath = Join-Path -Path $env:TEMP -ChildPath "temp_trigger_$(Get-Random).ps1"
        Set-Content -Path $tempScriptPath -Value $mockScript
        
        # Source the modified script
        . $tempScriptPath
        
        # Test the function with mock
        $result = Invoke-RemoteTrigger -ComputeHost "test-host" -User "test-user" -RemoteScript "~/test.sh" `
                                      -LocalHostName "localhost" -LocalIPAddress "127.0.0.1"
        
        if (-not $result.Success) {
            Write-Host "FAILED: Invoke-RemoteTrigger returned failure status" -ForegroundColor Red
            return $false
        }
        
        if ($result.Output -ne "Mocked SSH output - Success") {
            Write-Host "FAILED: Unexpected output from mocked function" -ForegroundColor Red
            return $false
        }
        
        Write-Host "PASSED: Invoke-RemoteTrigger correctly handled mocked SSH call" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "ERROR in test: $_" -ForegroundColor Red
        return $false
    }
    finally {
        # Remove the temporary script file
        if (Test-Path $tempScriptPath) {
            Remove-Item -Path $tempScriptPath -Force
        }
        
        # Re-source the original script
        . (Join-Path -Path $PSScriptRoot -ChildPath '..\experiments_nwb\trigger.ps1')
    }
}

# Run tests
$testResults = @(
    Test-GetAcquisitionHostInfo
    Test-InvokeRemoteTriggerMock
)

# Summarize results
$passedCount = ($testResults | Where-Object { $_ -eq $true }).Count
$failedCount = ($testResults | Where-Object { $_ -eq $false }).Count
$totalCount = $testResults.Count

Write-Host "`nTest Summary:" -ForegroundColor Cyan
Write-Host "  Total Tests: $totalCount" -ForegroundColor Cyan
Write-Host "  Passed: $passedCount" -ForegroundColor $(if ($passedCount -eq $totalCount) { "Green" } else { "Yellow" })
Write-Host "  Failed: $failedCount" -ForegroundColor $(if ($failedCount -eq 0) { "Green" } else { "Red" })

# Return overall success/failure
if ($failedCount -eq 0) {
    Write-Host "`nALL TESTS PASSED" -ForegroundColor Green
    exit 0
} else {
    Write-Host "`nSOME TESTS FAILED" -ForegroundColor Red
    exit 1
}
