#!/bin/bash

# Bash script to set up RASPI shutdown:

set -e # Exit on any error

# DO NOT CHANGE: This is the default path variables for MediaMTX.
# These variables are not meant to be changed to avoid unecessary
# compilations (path not found) and setup all over the place. Instread,
# a standardize approach 'convention over configuration' is set.
TARGET_VERSION="1.12.2" # MediaMTX version

WORKDIR=$(dirname $0) # The directory where the script is executed

TARGET_PATH=/opt/shutdown                         # Get the path to the script
BIN_PATH=$TARGET_PATH/shutdown.py                 # Shutdown python script
SYSTEMD_PATH=/etc/systemd/system/shutdown.service # MediaMTX systemd file path

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

# Check dependencies
check_dependencies() {
  log_info "Checking dependencies..."

  # Check for ffmpeg (needed for streaming)
  if ! command -v python &>/dev/null; then
    log_info "python is not found, installing..."
    sudo apt install ffmpeg
  else
    log_success "python is available"
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

do_copy_script() {
  check_workdir

  # Check if shutdown script already exists in current directory
  if [ -f $BIN_PATH ]; then
    log_success "Shutdown script already exists"
    return 0
  fi

  sudo cp main.py $BIN_PATH

  log_success "Shudown script copied"
}

do_create_service() {
  check_workdir

  # Check if service is not set up
  if [ -e $SYSTEMD_PATH ]; then
    log_success "Shutdown service already exists"
  fi

  # Write systemd service for shutdown service
  sudo tee $SYSTEMD_PATH >/dev/null <<EOF
[Unit]
Description=Shutdown
After=network.target

[Service]
ExecStart=python $BIN_PATH
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

  # Set shutdown service to start on boot
  sudo systemctl enable shutdown

  # Start shutdown service
  sudo systemctl start shutdown
}

# Entrypoint
main() {
  check_dependencies
  check_workdir
  do_copy_script
  do_create_service
}
main
