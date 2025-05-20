# MediaMTX Media Streaming

[Version 1.12.2](https://github.com/bluenviron/mediamtx/releases/tag/v1.12.2) | [Documentation](https://github.com/bluenviron/mediamtx)

> This program can only be run on Linux OS on the following architecture:
> 
> - x86_64
> 
> - arm64
> 
> - armv7l

## Run

### Prerequisite

Get the necessary dependencies:

- Ubuntu/Debian:
  
  ```bash
  sudo apt update && sudo apt get git wget ffmpeg ufw
  ```

### Execute

Execute `run_mediamtx.sh` to start the program. It can be run in any path (not neccessarily in the script folder. The script will perform the following actions:

1. Install `mediamtx`

2. Create `mediamtx.yml` 

3. Execute `mediamtx`

The location of the installed `mediamtx` and its config file `mediamtx.yml` are located within the same location as `run_mediamtx.sh`.

```
<path/to/folder>
├── mediamtx [after script first run]
├── mediamtx.yml [after script first run]
├── mediamtx.yml.sample [backup - do not remove]
├── README.md
└── run_mediamtx.sh [main script]
```

Streaming endpoints:

- Publish the income or source stream to `rtmp://<ip_address>:1935/live`.

- Stream HLS protocol (with playback) through `http://<ip_address>:8888/live`.

- Stream WebRTC protocol (low latency) through `http://<ip_address>:8889/live_opus`.

- Update the YouTube RTMP key inside the `mediamtx.yml` (generated after running the script for the first time). Use the keyword `<stream-key>` for faster lookup and replace it with an actual YouTube Stream Key.

### Cronjob

To setup Cronjob so that the program can be started on boot:

1. Execute `echo $(pwd)/run_mediamtx.sh` at where the `run_mediamtx.sh` is located. Then, copy the output.

2. Run `sudo crontab -e`

3. Choose `option 1` with `nano`

4. Paste the output.

### Firewall

Run the following commands to setup the firewall:

```bash
# Enable firewall on startup
sudo ufw enable
 
sudo ufw allow OpenSSH # SSH port 22
sudo ufw allow 8888 # HLS port
sudo ufw allow 8889 # WebRTC port
sudo ufw allow 1935 # RTMP port
sudo ufw allow 8554 # RTSP port
```


