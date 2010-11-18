#!/bin/bash

# This script unloads and then loads the Broadcom b43 kernel module
echo 'Your Password is needed to unload/load the Broadcom b43 kernel module'
sudo modprobe -r b43
sudo modprobe b43


