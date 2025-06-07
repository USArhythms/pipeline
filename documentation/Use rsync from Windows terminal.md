
## Use `rsync` in Windows Terminal

### Install MSYS2.
Follow the [MSYS2 installation guide](https://www.msys2.org/).
  
Add the MSYS2 `usr/bin` directory to your Windows `PATH`.
   For example, if MSYS2 is installed in `C:\msys64`, add `C:\msys64\usr\bin` to your `PATH`.
   To do this:  
   1. Right-click on "This PC" or "Computer" on your desktop or in File Explorer.
   2. Click on "Properties".
   3. Click on "Advanced system settings".
   4. Click on the "Environment Variables" button.
   5. In the "System variables" section, find the `Path` variable and click "Edit".
   6. Add a new entry for `C:\msys64\usr\bin` (or wherever MSYS2 is installed).
   7. Click "OK" to close all dialog boxes.

---

### Install `rsync` within MSYS2 — it’s not included by default.

1. Open the MSYS2 Shell

   * Run `MSYS2 MSYS` from your Start menu or search bar.

2. Update MSYS2 (Optional but Recommended)
   Before installing packages, update the package database and core system packages:
   ```bash
   pacman -Syu
   ```
   > If prompted to restart MSYS2 after updating core packages, close the shell and reopen it, then run:
   ```bash
   pacman -Su
   ```

3. Install `rsync`, `openssh` and dependencies
   ```bash
   pacman -S rsync openssh libzstd libxxhash
   ```

4. Verify Installation
   In the same MSYS2 shell:
   ```bash
   rsync --version
   ```

---

### Install Clink
To enhance your command line experience, you can install [Clink](https://chrisant996.github.io/clink/).
1. Download the latest Clink release from [Clink Releases](https://github.com/chrisant996/clink/releases). 
2. Extract the downloaded archive to a directory of your choice (e.g., `C:\clink`).
3. Add the Clink directory to your Windows `PATH` environment variable:
   - Right-click on "This PC" or "Computer" on your desktop or in File Explorer.
   - Click on "Properties".
   - Click on "Advanced system settings".
   - Click on the "Environment Variables" button.
   - In the "System variables" section, find the `Path` variable and click "Edit".
   - Add a new entry for `C:\clink` (or wherever you extracted Clink).
   - Click "OK" to close all dialog boxes.

---

### Quick Test in Windows Terminal 

To verify it's working:

```cmd
where rsync
rsync --version
```

Some `rsync` commands may not work directly in the Windows Command Prompt or PowerShell due to path issues. If so, prepend the command with the MSYS2 bash shell to ensure it runs correctly:  
```cmd
C:\msys64\usr\bin\bash.exe -lc "rsync -Pavu /d/MyData/... me@host:remote/dir"
```

Alternatively, you can add MSYS2 to the Windows Terminal as a profile, allowing you to run `rsync` commands directly in the MSYS2 environment.

1. Launch **Windows Terminal**.
2. Press `Ctrl` + `Shift` + `P` to open the **Command Palette**.
3. Type and select **"Open settings (JSON)"**.
4. Add the profiles for MSYS2 in the `settings.json` file.
Paste the following inside the `"profiles": { "list": [ ... ] }` array.

* MSYS2 base shell (POSIX environment)

```json
{
  "name": "MSYS2: msys2",
  "commandline": "C:/msys64/msys2_shell.cmd -defterm -here -no-start -msys2 -shell bash",
  "startingDirectory": "%USERPROFILE%",
  "icon": "C:/msys64/msys2.ico"
}
```

* MSYS2 Mingw64 shell (64-bit toolchain)

```json
{
  "name": "MSYS2: mingw64",
  "commandline": "C:/msys64/msys2_shell.cmd -defterm -here -no-start -mingw64 -shell bash",
  "startingDirectory": "%USERPROFILE%",
  "icon": "C:/msys64/mingw64.ico"
}
```

5. Save the `settings.json` file.
6. Close the editor.
7. Restart **Windows Terminal**.

You’ll now see:

* `MSYS2: msys2`
* `MSYS2: mingw64`

...in the dropdown menu.