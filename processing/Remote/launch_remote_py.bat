@echo off
:: =========================================================================
:: launch_remote_py.bat - Launch Python Trigger Script
:: =========================================================================
::
:: DESCRIPTION:
::   This batch file executes the Python trigger script that connects to
::   a remote compute server to initiate post-acquisition processing.
::   It runs the script in the current console window, allowing the user
::   to see any output or error messages directly.
::
:: USAGE:
::   launch_remote_py.bat
::
:: REQUIREMENTS:
::   - Python must be installed and in the system PATH
::   - The trigger.py script must be in the same directory as this batch file
::   - The paramiko Python package must be installed (for SSH functionality)
::
:: NOTES:
::   - No parameters are required
::   - Alternative to launch_remote_ps.bat which uses PowerShell instead
::
:: =========================================================================

echo Starting Python trigger script...

:: Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

:: Change to the script directory to ensure relative paths work
cd /d "%SCRIPT_DIR%"

:: Execute the Python script
python trigger.py

echo Python trigger script execution completed.
pause