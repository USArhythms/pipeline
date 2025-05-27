# **Neurodata backup and launch scripts**

The files in **backup-scripts** are intended to be installed on instrumentation/acquisition computers for regular/systematic backups to a local or remote server. They are also useful for subsequent processing, such as submission to a computing cluster, NWB conversion prep (see **post-acquisition** and **experiments_nwb** folders).  

This is work in progress. If you have additional scripts that may be useful in processing (automatic calculations, file transfer, etc), and wish to share with U19 consortium, please contact: drinehart@ucsd.edu.

## Windows acquisition computer (Widefield @ UCSD) scripts:

1. GitHub clone [TBD](https://github.com/update_this.git) to a local directory (e.g., `C:\Data\Backups`).
2. Install [SyncBackPro](https://www.2brightsparks.com/syncback/sbpro.html)
3. Setup configuration in SyncBackPro:
   * If the server is is mapped in Windows or accessible via a network share (i.e., a "local" server), then load the `data_sync.sps` settings in the application. 
   Export/Import menu > Import Profile > Select `data_sync.sps` file from the cloned repository.  
   If asked about allowing empty passwords, select "No" to avoid security issues.  
   Then right click on the profile in SyncBackPro and select "Modify" to modify the settings for:
   - Backup configuration
   - Email notification destination
   - Location of local data acquisition directories

   * If the remote server is a sftp server, then -- right now create a new profile manually ...
   Managed to connnect using my SSH key with FTP Engines Eldos, DevArt or Chilkat, but not WeOnlyDo, whatever that is. The difference betweeen engines is not documented. 

   * Ensure the server where files will be stored has correct permissions for the user account that will be used to transfer files.

   * Verify which parsing script will be run before/after transfer.

   * Edit (using a text editor) `launch.bat` or `launch_remote.bat` to run the correct parsing command, as appropriate.
      - **Note**: `launch.bat` example runs a MATLAB script on the acquisition computer.
      - **N.B.** `launch_remote_py.bat` runs `trigger.py` (see additional notes in [README-trigger.md](README-trigger.md)).
      - **N.B.2** `launch_remote_ps.bat` runs `trigger.ps1` (see additional notes in [README-trigger_ps.md](README-trigger_ps.md)).



+ [README-ssh_windows_linux.md](README-ssh_windows_linux.md) to setup password-less SSH from Windows to Linux
  

## Post-acquisition server (linux):

In example above where post-acquisition will occur, ensure script exists (Matlab or python).  
This step should include any formatting/analysis required after acquisition as well as meta-data extraction into NWB recordings files (Excel/csv)

Example bash script for launching server-side scripts: post-acquisition/post-acquire.sh

## Features

- Nightly transfer of data from acquisition computer to local storage computer
- Email notification of transferred files
- Ability to integrate with other applications (compute/interim calcs, appending to lab notebook/database, conversion to NWB format)


## Contribute

[Issue Tracker] (https://github.com/USArhythms/pipeline/issues)

[Source Code] (https://github.com/USArhythms/pipeline)

## Support

If you are having issues or questions; or have code to contribute, please let me know.
Duane Rinehart
drinehart[at]ucsd.edu

## License

The project is licensed under the [MIT license](https://mit-license.org/).

---
Last update: 13-DEC-2024
