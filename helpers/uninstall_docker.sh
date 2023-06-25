#!/bin/bash

set -e

read -p "This script will remove Docker. Do you want to continue? (y/n) " confirm
if [ "$confirm" != "y" ]; then
  printf "Aborting."
  exit 1
fi

printf "Removing Docker packages and files...\n"
dpkg -l | grep -i docker
sudo apt-get remove -y docker-engine docker docker.io docker-ce docker-ce-cli docker-compose-plugin
sudo apt-get autoremove -y
sudo rm -rf /var/lib/docker /etc/docker
sudo rm -f /etc/apparmor.d/docker
sudo groupdel docker
sudo rm -rf /var/run/docker.sock

printf "Docker has been completely removed from your system."