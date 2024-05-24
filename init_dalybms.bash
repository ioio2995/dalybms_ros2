#!/bin/bash
# Bash script for setup dalybms env
# Author: Lionel ORCIL - github.com/ioio2995
#
# Specify the path of the directory to check

# Install apt deps
sudo apt update
sudo apt install python3-pip

# Install pip deps
pip3 install pyserial dalybms