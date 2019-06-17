#!/bin/bash

# Only root can run this script
if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root" 2>&1
  exit 1
fi

echo "Copying file to /usr/bin/BinaryPatcher.py"
sudo cp BinaryPatcher.py /usr/bin/BinaryPatcher.py
echo "Adding +x flag to /usr/bin/BinaryPatcher.py"
sudo chmod +x /usr/bin/BinaryPatcher.py

echo
echo "Done!"
