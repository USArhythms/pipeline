# **Neurodata pipeline processing scripts**

***Scripts*** may be installed on instrumentation/acquisition computers for regular/systematic backups to local server.  They are also useful for subsequent processing (such as submission to cluster for calculations, NWB conversion prep)

This is work in progress. If you have additional scripts that may be useful in processing (automatic calculations, file transfer, etc), and wish to share with U19 consortium, please contact: drinehart@ucsd.edu.

## Windows acquisition computer (Widefield @ UCSD) scripts:

1. GitHub clone [USArhythms pipeline](https://github.com/USArhythms/pipeline.git) to a local directory (e.g., `C:\experiments_nwb`).
2. Install [SyncBackPro](https://www.2brightsparks.com/syncback/sbpro.html) and load the `data_sync.sps` settings in the application.
3. Modify settings in SyncBackPro for:
   - Backup configuration
   - Email notification destination
   - Location of local data acquisition directories

   a. Ensure the local server where files will be stored has correct permissions and is mapped in Windows.

   b. Verify which parsing script will be run before/after transfer.

   c. Edit (using a text editor) `launch.bat` or `launch_remote.bat` to run the correct parsing command, as appropriate.
      - **Note**: `launch.bat` example runs a MATLAB script on the acquisition computer.
      - **N.B.** `launch_remote.bat` runs `trigger.py` (see additional notes in [README-trigger.md](README-trigger.md)).



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
Last update: 18-NOV-2024
