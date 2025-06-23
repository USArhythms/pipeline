# Set up WinSCP

Download and install [WinSCP](https://winscp.net/).

## Configure a new site profile

1. Launch **WinSCP** and click *New Site*.
2. Set the **File protocol** to **SFTP**.
3. Enter the host name, port number (typically 22), and username for the remote server.
4. Under **Advanced → Authentication** specify the path to your [private SSH key](backup-scripts\README-ssh_windows_linux.md) if passwordless login is configured.
5. Save the site with a specific name (e.g, `NESE_backup`).

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
open "NESE_backup"
put -delete C:\\Data\\MyProject\\* /remote/backup/dir
exit
```
You can also use the **Synchronize** feature to keep directories in sync.

```batch
option batch on
option confirm off
open "NESE_backup"
synchronize remote -delete C:\\Data\\MyProject\\ /remote/backup/dir
exit
```

Run the script using the command line:

```cmd
"C:\\Program Files (x86)\\WinSCP\\WinSCP.exe" /script="C:\\Path\\To\\backup_script.txt"
```

Use the Windows Task Scheduler to run the command regularly for automated backups.
For example, you can set it to run daily at a specific time: 
1. Open **Task Scheduler**.
2. In the **Action** menu, click **Create Basic Task**.
3. Name the task and set the trigger to daily.
4. In the action step, select **Start a program** and enter the command to run WinSCP with your script.
5. Finish the setup and ensure the task is enabled.
