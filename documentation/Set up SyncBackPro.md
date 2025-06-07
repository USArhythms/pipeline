Install [SyncBackPro](https://www.2brightsparks.com/syncback/sbpro.html)

Setup configuration in SyncBackPro:
   * If the server is is mapped in Windows or accessible via a network share (i.e., a "local" server), then load the `data_sync.sps` settings in the application. 
   Export/Import menu > Import Profile > Select `data_sync.sps` file from the cloned repository.  
   If asked about allowing empty passwords, select "No" to avoid security issues.  
   Then right click on the profile in SyncBackPro and select "Modify" to modify the settings for:
   - Backup configuration
   - Email notification destination
   - Location of local data acquisition directories

   * If the remote server is a sftp server, then create a new profile manually [To be documented].
   Connect using your SSH key with FTP Engines Eldos, DevArt or Chilkat. Do not use WeOnlyDo (the difference betweeen engines is not documented). 

   * Ensure the server where files will be stored has correct permissions for the user account that will be used to transfer files.