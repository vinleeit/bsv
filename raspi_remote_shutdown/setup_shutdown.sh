#!/bin/bash

# Bash script to set up RASPI shutdown:

set -e # Exit on any error

# DO NOT CHANGE: This is the default path variables for MediaMTX.
# These variables are not meant to be changed to avoid unecessary
# compilations (path not found) and setup all over the place. Instread,
# a standardize approach 'convention over configuration' is set.
TARGET_VERSION="1.12.2" # MediaMTX version

WORKDIR=$(dirname $0) # The directory where the script is executed

TARGET_DIR=/opt/shutdown                          # Get the path to the script
BIN_PATH=$TARGET_DIR/shutdown.py                  # Shutdown python script
ENV_PATH=$TARGET_DIR/.env                         # Dotenv path
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
  if ! command -v sudo python3 &>/dev/null; then
    log_info "python is not found, installing..."
    sudo apt install python3
  else
    log_success "python is available"
  fi

  if ! sudo python3 -c "import dotenv" 2>/dev/null; then
    log_info "python-dotenv is not found, installing..."
    sudo apt install python3-dotenv
  else
    log_success "python-dotenv is available"
  fi
}

check_workdir() {
  if [ -d $TARGET_DIR ]; then
    return 0
  fi

  log_info "Directory '$TARGET_DIR' is not found, creating..."

  # Workdir is not found
  mkdir $TARGET_DIR

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

do_copy_dotenv() {
  check_workdir

  if [ -f $ENV_PATH ]; then
    log_success "Dotenv file already exists"
    return 0
  fi

  sudo cp sample.env $ENV_PATH
  log_success "Dotenv file copied"
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
ExecStart=python3 $BIN_PATH
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

  # Set shutdown service to start on boot
  sudo systemctl enable shutdown

  # Start shutdown service
  sudo systemctl start shutdown
}

do_install() {
  # Check if running as root/sudo
  if [[ $EUID -ne 0 ]]; then
    log_error "Installation requires root privileges. Run with sudo."
    exit 1
  fi

  check_dependencies
  check_workdir
  do_copy_script
  do_copy_dotenv
  do_create_service
  log_success "Installation success"
}

do_uninstall() {
  # Check if running as root/sudo
  if [[ $EUID -ne 0 ]]; then
    log_error "Uninstallation requires root privileges. Run with sudo."
    exit 1
  fi

  if [ -e $SYSTEMD_PATH ]; then
    sudo systemctl stop shutdown
    sudo systemctl disable shutdown
    sudo rm $SYSTEMD_PATH
    log_success "Shutdown service has been removed"
  fi

  if [ -e $BIN_PATH ]; then
    sudo rm $BIN_PATH
    log_success "$BIN_PATH has been removed"
  fi

  if [ -e $ENV_PATH ]; then
    sudo rm $ENV_PATH
    log_success "$ENV_PATH has been removed"
  fi

  if [[ -z "$(ls -A $TARGET_DIR 2>/dev/null)" ]]; then
    sudo rm -r $TARGET_DIR
    log_success "$TARGET_DIR has been removed"
  else
    log_warning "$TARGET_DIR contains other non-system files thus will have to be removed manually"
  fi

  log_success "Uninstallation success"
}

show_help() {
  cat <<EOF
Usage: $0 [OPTIONS]

A simple CLI tool with install and uninstall capabilities.

OPTIONS:
    -h, --help      Show this help message and exit
    -i, --install   Install the tool to system PATH
    -u, --uninstall Uninstall the tool from system PATH

EXAMPLES:
    $0 -h           Display help
    $0 -i           Install tool to $INSTALL_DIR
    $0 -u           Remove tool from $INSTALL_DIR

EOF
}

# Parse command line arguments
case "${1:-}" in
-h | --help)
  show_help
  exit 0
  ;;
-i | --install)
  do_install
  exit 0
  ;;
-u | --uninstall)
  do_uninstall
  exit 0
  ;;
"")
  show_help
  ;;
*)
  echo "Error: Unknown option '$1'"
  echo "Use '$0 -h' for help."
  exit 1
  ;;
esac
