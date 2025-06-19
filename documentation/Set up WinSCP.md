# Set up WinSCP

Download and install [WinSCP](https://winscp.net/).

## Configure a new site profile

1. Launch **WinSCP** and click *New Site*.
2. Set the **File protocol** to **SFTP**.
3. Enter the host name, port number (typically 22), and username for the remote server.
4. Under **Advanced → Authentication** specify the path to your private SSH key if passwordless login is configured.
5. Save the site with a memorable name.

## Transfer files manually

1. Select the site profile and click **Login**.
2. Drag and drop files between the local pane and the remote pane to copy data.
3. You can also right‑click on files or folders to queue them for transfer.

## Automate transfers with a script

WinSCP can run from the command line or a batch file.
An example script (`backup_script.txt`) might look like:

```batch
option batch on
option confirm off
open "MySite"
put -delete C:\\Data\\MyProject\\* /remote/backup/dir
exit
```

Run it with:

```cmd
winscp.com /script=backup_script.txt
```

Use the Windows Task Scheduler to run the command regularly for automated backups.
