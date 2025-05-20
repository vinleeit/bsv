#!/bin/bash

# MediaMTX Installation Script
# This script downloads, extracts, and configures MediaMTX if not already installed

WORKDIR=$(dirname $0)
TARGET_VERSION="1.12.2"

# Check if mediamtx executable already exists in current directory
if [ ! -f "${WORKDIR}/mediamtx" ]; then
  echo "Performing MediaMTX installation..."

  # Detect system architecture
  ARCH=$(uname -m)
  case $ARCH in
  x86_64 | amd64)
    TARGET_ARCH="amd64"
    ;;
  aarch64 | arm64)
    TARGET_ARCH="arm64"
    ;;
  armv7l | armv7)
    TARGET_ARCH="armv7"
    ;;
  *)
    echo "Unsupported architecture: $ARCH"
    echo "Please manually download the appropriate go2rtc binary for your system"
    exit 1
    ;;
  esac

  echo "Downloading MediaMTX for $ARCH..."
  DOWNLOAD_URL="https://github.com/bluenviron/mediamtx/releases/download/v${TARGET_VERSION}/mediamtx_v${TARGET_VERSION}_linux_${TARGET_ARCH}.tar.gz"
  wget -q "$DOWNLOAD_URL" -O ${WORKDIR}/mediamtx.tar.gz
  if [ $? -ne 0 ]; then
    echo "Download failed."
    exit 1
  fi

  # Extract only the mediamtx executable directly
  echo "Installing..."
  tar -xzf ${WORKDIR}/mediamtx.tar.gz -C ${WORKDIR} --wildcards "mediamtx"

  # Make the executable... executable
  chmod +x ${WORKDIR}/mediamtx

  # Remove the downloaded tar file
  rm -f ${WORKDIR}/mediamtx.tar.gz

  echo "MediaMTX has been installed successfully."
fi

# Create configuration file if it doesn't exist
if [ ! -f "${WORKDIR}/mediamtx.yml" ]; then
  echo "mediamtx.yml file is not found, copying sample..."
  cp ${WORKDIR}/mediamtx.yml.sample ${WORKDIR}/mediamtx.yml
  echo "mediamtx.yml is successfully copied."
fi

# Execute MediaMTX
echo "Starting MediaMTX..."
${WORKDIR}/mediamtx ${WORKDIR}/mediamtx.yml
