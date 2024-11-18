# **Neurodata pipeline processing scripts**

***Scripts*** may be installed on instrumentation/acquisition computers for regular/systematic backups to local server.  They are also useful for subsequent processing (such as submission to cluster for calculations, NWB conversion prep)

This is work in progress. If you have additional scripts that may be useful in processing (automatic calculations, file transfer, etc), and wish to share with U19 consortium, please contact: drinehart@ucsd.edu.

## Windows acquisition computer (Widefield @ UCSD) scripts:

    1. github clone https://github.com/USArhythms/pipeline.git [on local storage such as C:\experiments_nwb]
    2. Install [SyncBackPro] (https://www.2brightsparks.com/syncback/sbpro.html) and load data_sync.sps settings in application
    3. Modify settings in SyncBackPro for backup, e-mail notification destination, and location of local data acquisition directories
    3a. Ensure local server where files will be stored has correct permissions and is mapped in Windows
    3b. Verify which parsing script will be run before/after transfer (currently parse_widefield.m)
    3c. Edit (text editor) launch.bat script to run correct parsing command, as appropriate
    4. For post-processing, you may also need remote execution on server. 
        To setup password-less SSH from Windows to Linux, see README-ssh_windows_linux below

+ See [README-ssh_windows_linux.md](README-ssh_windows_linux.md) for detailed instructions
  
## Features

---

- Nightly transfer of data from acquisition computer to local storage computer
- Email notification of transferred files
- Ability to integrate with other applications (compute/interim calcs, appending to lab notebook/database, conversion to NWB format)


## Contribute

---

[Issue Tracker] (https://github.com/USArhythms/pipeline/issues)

[Source Code] (https://github.com/USArhythms/pipeline)

## Support

---

If you are having issues or questions; or have code to contribute, please let me know.
Duane Rinehart
drinehart[at]ucsd.edu

## License

---
The project is licensed under the [MIT license](https://mit-license.org/).

---
Last update: 17-OCT-2024
