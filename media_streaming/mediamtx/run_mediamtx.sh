#!/bin/bash

# Bash script to set up MediaMTX:
# - Check system architecture compatibility
# - Check if MediamMTX is already installed or running
# - Download MediaMTX binary
# - Check if MediaMTX config is exist
# - Write MediaMTX config
# - Check if MediaMTX systemd service is set up
# - Write and enable MediaMTX systemd service

set -e # Exit on any error

# DO NOT CHANGE: This is the default path variables for MediaMTX.
# These variables are not meant to be changed to avoid unecessary
# compilations (path not found) and setup all over the place. Instread,
# a standardize approach 'convention over configuration' is set.
TARGET_VERSION="1.12.2" # MediaMTX version

WORKDIR=$(dirname $0)                         # The directory where the script is executed
CONFIG_SAMPLE_PATH=$WORKDIR/config.yml.sample # Sample MediaMTX config path

TARGET_PATH=/opt/mediamtx                         # Get the path to the script
BIN_PATH=$TARGET_PATH/mediamtx                    # MediaMTX binary path
CONFIG_PATH=$TARGET_PATH/config.yml               # MediaMTX config path
SYSTEMD_PATH=/etc/systemd/system/mediamtx.service # MediaMTX systemd file path

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
  echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
  echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
  echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

# Detect OS and architecture
check_platform() {
  # Detect system architecture
  local arch=$(uname -m)
  case $arch in
  x86_64 | amd64)
    target_arch="amd64"
    ;;
  aarch64 | arm64)
    target_arch="arm64"
    ;;
  armv7l | armv7)
    target_arch="armv7"
    ;;
  *)
    log_error "Unsupported architecture: $arch\nPlease manually download the appropriate go2rtc binary for your system"
    exit 1
    ;;
  esac
  log_success "$arch architecture is supported"
}

# Check dependencies
check_dependencies() {
  log_info "Checking dependencies..."

  # Check for ffmpeg (needed for streaming)
  if ! command -v ffmpeg &>/dev/null; then
    log_info "ffmpeg is not found, installing..."
    sudo apt install ffmpeg
  else
    log_success "ffmpeg is available"
  fi

  # Check for wget (needed to download mediamtx)
  if ! command -v curl &>/dev/null; then
    log_info "curl is not found, installing..."
    sudo apt install curl
  else
    log_success "curl is available"
  fi
}

check_workdir() {
  if [ -d $TARGET_PATH ]; then
    return 0
  fi

  log_info "Directory '$TARGET_PATH' is not found, creating..."

  # Workdir is not found
  mkdir $TARGET_PATH

  log_success "Successfully created workdir"
}

do_download_mediamtx() {
  check_workdir

  # Check if mediamtx executable already exists in current directory
  if [ -f $BIN_PATH ]; then
    log_success "MediaMTX binary already exists"
    return 0
  fi

  local download_url="https://github.com/bluenviron/mediamtx/releases/download/v${TARGET_VERSION}/mediamtx_v${TARGET_VERSION}_linux_${target_arch}.tar.gz"
  log_info "Downloading MediaMTX from: $download_url"
  curl -L --progress-bar $download_url | tar xz --wildcards "mediamtx"
  if [ $? -ne 0 ]; then
    echo "Download failed"
    exit 1
  fi

  if ! cmp -s mediamtx $BIN_PATH; then
    mv mediamtx $BIN_PATH -f
  fi

  # Make the executable... executable
  chmod +x $BIN_PATH

  log_success "MediaMTX binary downloaded and extracted"
}

do_create_config() {
  check_workdir

  # Create configuration file if it doesn't exist
  if [ -f $CONFIG_PATH ]; then
    log_success "MediaMTX config already exists"
    return 0
  fi

  log_info "Creating MediaMTX configuration..."
  cp $CONFIG_SAMPLE_PATH $CONFIG_PATH
  log_success "MediaMTX configuration created"
}

do_create_service() {
  check_workdir

  # Check if service is not set up
  if [ -e $SYSTEMD_PATH ]; then
    log_success "MediaMTX service already exists"
  fi

  # Write systemd service for MediaMTX
  sudo tee $SYSTEMD_PATH >/dev/null <<EOF
[Unit]
Description=MediaMTX Streamer
After=network.target

[Service]
#User=<your_user>  # The user under which MediaMTX will run
#Group=<your_group> # The group to which the user belongs
#WorkingDirectory=/home/<your_user>  # The working directory for MediaMTX
ExecStart=$BIN_PATH $CONFIG_PATH
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

  # Set GO2RTC to start on boot
  sudo systemctl enable mediamtx

  # Start GO2RTC
  sudo systemctl start mediamtx
}

# Entrypoint
main() {
  check_platform
  check_dependencies
  check_workdir
  do_download_mediamtx
  do_create_config
  do_create_service
}
main
