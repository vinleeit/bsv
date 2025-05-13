#!/bin/bash

# Check if go2rtc_linux_amd64 and config.yaml exist in the current directory
if [ ! -f "go2rtc_linux_amd64" ] || [ ! -f "config.yaml" ]; then
  echo "go2rtc files not found in current directory. Installing..."

  # Create config file if it doesn't exist
  if [ ! -f "config.yaml" ]; then
    echo "Creating config.yaml..."
    touch config.yaml
  fi

  # Download go2rtc binary if it doesn't exist
  if [ ! -f "go2rtc_linux_amd64" ]; then
    echo "Downloading go2rtc binary..."
    wget https://github.com/AlexxIT/go2rtc/releases/download/v1.9.9/go2rtc_linux_amd64

    # Make the binary executable
    chmod +x go2rtc_linux_amd64
  fi

  echo "Installation complete."
fi

# Run go2rtc
echo "Starting go2rtc..."
./go2rtc_linux_amd64 -c ./config.yaml
