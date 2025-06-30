# Raspi Remote Shutdown

A simple TCP server listening for shutdown request.

## How To Run

1. Clone git repository.

2. `cd` to the cloned directory.

3. Run the following to start installation:
   
   ```bash
   # Option 1
   sudo ./setup_shutdown.sh -i
   
   # Option 2
   sudo ./setup_shutdown.sh --install
   ```
   
   The shutdown program will be installed at `/opt/shutdown` folder alongside the `.env` file. To configure the program, edit the `/opt/shutdown/.env` file. e.g.
   
   ```bash
   # /opt/shutdown/.env
   
   # Server hosted at localhost, change to 0.0.0.0 for access
   # in the local network.
   SERVER_HOST='127.0.0.1'
   
   # Default server port
   SERVER_PORT=4000
   
   # Filtered IPs that are allowed to communicate with the server,
   # only respect regex format.
   ALLOWED_ORIGIN='*'
   ```
   
   Run `sudo systemctl restart shutdown` to restart the program with the new configuration.
   
   By default, the shutdown program will start on every system boot, to disable or re-enable run the following commands:
   
   ```bash
   # disable
   sudo systemctl disable shutdown
   
   # enable
   sudo systemctl enable shutdown
   ```
   
   To start or stop the shutdown program, run the following commands:
   
   ```bash
   # stop
   sudo systemctl stop shutdown
   
   # start
   sudo systemctl start shutdown
   ```
   
   To configure the `systemd` settings such as restart interval and restart on fail, edit the `/etc/systemd/system/shutdown.service` file and run the `sudo systemctl restart shutdown` to apply the new setting.

4. Run the following to get help:
   
   ```bash
   # Option 1
   ./setup_shutdown.sh
   
   # Option 2
   ./setup_shutdown.sh -h
   
   # Option 3
   ./setup_shutdown.sh --help 
   ```

5. Run the following to uninstall:
   
   ```bash
   # Option 1
   sudo ./setup_shutdown.sh -u
   
   # Option 2
   sudo ./setup_shutdown.sh --uninstall
   ```
   
   The `--uninstall` flag will remove all files related to shutdown program, including the `/opt/shutdown` folder. However, if there is anything not related to shutdown program exists within the folder, the folder will be left and needed to be manually removed.


