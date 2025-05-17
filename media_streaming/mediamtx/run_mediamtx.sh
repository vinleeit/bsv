#!/bin/bash

# MediaMTX Installation Script
# This script downloads, extracts, and configures MediaMTX if not already installed

# Check if mediamtx executable already exists in current directory
if [ -f "./mediamtx" ]; then
  echo "MediaMTX is already installed."
else
  echo "Installing MediaMTX..."

  # Determine architecture
  ARCH=$(uname -m)
  DOWNLOAD_URL=""
  MEDIAMTX_VERSION="1.12.2"

  if [ "$ARCH" = "x86_64" ]; then
    DOWNLOAD_URL="https://github.com/bluenviron/mediamtx/releases/download/v${MEDIAMTX_VERSION}/mediamtx_v${MEDIAMTX_VERSION}_linux_amd64.tar.gz"
  elif [ "$ARCH" = "aarch64" ]; then
    DOWNLOAD_URL="https://github.com/bluenviron/mediamtx/releases/download/v${MEDIAMTX_VERSION}/mediamtx_v${MEDIAMTX_VERSION}_linux_arm64.tar.gz"
  else
    echo "Unsupported architecture: $ARCH"
    exit 1
  fi

  # Download the appropriate tar file
  echo "Downloading MediaMTX for $ARCH..."
  wget -q "$DOWNLOAD_URL" -O mediamtx.tar.gz

  if [ $? -ne 0 ]; then
    echo "Download failed."
    exit 1
  fi

  # Extract only the mediamtx executable directly
  echo "Extracting the mediamtx executable..."
  tar -xzf mediamtx.tar.gz --wildcards "mediamtx"

  # Make the executable... executable
  echo "Installing..."
  chmod +x ./mediamtx

  # Remove the downloaded tar file
  rm -f mediamtx.tar.gz

  echo "MediaMTX has been installed successfully."
fi

# Create configuration file if it doesn't exist
if [ ! -f "./mediamtx.yml" ]; then
  echo "mediamtx.yml file is not found, copying sample..."
  cp mediamtx.yml.sample mediamtx.yml
  echo "mediamtx.yml is successfully copied."
fi

# Execute MediaMTX
echo "Starting MediaMTX..."
./mediamtx
