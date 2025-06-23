@echo off
:: =========================================================================
:: launch_remote_ps.bat - Launch PowerShell Trigger Script
:: =========================================================================
::
:: DESCRIPTION:
::   This batch file launches the PowerShell trigger script in a new window.
::   It uses the RemoteSigned execution policy to allow the script to run
::   while maintaining security. The script is launched asynchronously
::   to allow the caller to continue with other tasks.
::
:: USAGE:
::   launch_remote_ps.bat
::
:: NOTES:
::   - No parameters are required
::   - The path to the trigger.ps1 script may need to be adjusted if moved
::   - Requires PowerShell to be installed on the system
:: 
:: ========================================================================

echo Starting PowerShell trigger script in a new window...

:: Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

:: Launch PowerShell script using a relative path (from the batch file location)
start "" Powershell.exe -ExecutionPolicy RemoteSigned -File "%SCRIPT_DIR%trigger.ps1"

echo Trigger script launched. Check the new window for progress.
