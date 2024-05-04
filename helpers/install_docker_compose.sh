#!/bin/bash

set -e

printf "Removing existing docker-compose installation, if any...\n"
sudo rm /usr/local/bin/docker-compose || true

printf "Downloading and install the latest version of docker-compose...\n"
COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4)
sudo curl -L "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

printf "Checking that docker-compose is installed successfully...\n"
sudo docker compose version
