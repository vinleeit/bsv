#!/bin/bash

# Detect system architecture
ARCH=$(uname -m)
case $ARCH in
x86_64)
  GO2RTC_ARCH="amd64"
  ;;
aarch64 | arm64)
  GO2RTC_ARCH="arm64"
  ;;
*)
  echo "Unsupported architecture: $ARCH"
  echo "Please manually download the appropriate go2rtc binary for your system"
  exit 1
  ;;
esac

GO2RTC_BINARY="go2rtc_linux_${GO2RTC_ARCH}"
GO2RTC_VERSION="1.9.9"
GO2RTC_URL="https://github.com/AlexxIT/go2rtc/releases/download/v${GO2RTC_VERSION}/${GO2RTC_BINARY}"

# Check if go2rtc binary and config.yaml exist in the current directory
if [ ! -f "$GO2RTC_BINARY" ] || [ ! -f "config.yaml" ]; then
  echo "go2rtc files not found in current directory. Installing..."

  # Create config file if it doesn't exist
  if [ ! -f "config.yaml" ]; then
    echo "config.yaml file is not found, copying sample..."
    cp config.yaml.sample config.yaml
    echo "config.yaml sample has been copied."
  fi

  # Download go2rtc binary if it doesn't exist
  if [ ! -f "$GO2RTC_BINARY" ]; then
    echo "Downloading go2rtc binary for $ARCH architecture ($GO2RTC_ARCH)..."
    wget "$GO2RTC_URL"

    # Make the binary executable
    chmod +x "$GO2RTC_BINARY"
  fi

  echo "Installation complete."
fi

# Run go2rtc
echo "Starting go2rtc..."
./"$GO2RTC_BINARY" -c ./config.yml
