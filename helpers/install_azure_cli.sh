#!/bin/bash

set -e

printf "Adding the Microsoft package signing key to trusted keys...\n"
curl -sL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/microsoft.gpg > /dev/null

AZ_REPO=$(lsb_release -cs)
printf "Adding the Azure CLI repository to the package manager...\n"
echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ $AZ_REPO main" | sudo tee /etc/apt/sources.list.d/azure-cli.list

printf "Installing the Azure CLI...\n"
sudo apt-get install azure-cli -y

printf "Azure CLI has been installed successfully."