#!/bin/bash

set -e

DIST="$(lsb_release -is)"
case "$DIST" in
    Debian)
        DIST_URL="debian"
        ;;
    Ubuntu)
        DIST_URL="ubuntu"
        ;;
    *)
        printf "Distribution $DIST not supported"
        exit 1
        ;;
esac

GPG_ADDR="https://download.docker.com/linux/$DIST_URL/gpg"
DIST_ADDR="https://download.docker.com/linux/$DIST_URL"

printf "Adding the Docker repository and installing dependencies...\n"
sudo apt-get remove docker docker-engine docker.io containerd runc || true

sudo apt-get update -y
sudo apt-get install -y \
  ca-certificates \
  curl \
  gnupg \
  lsb-release

sudo mkdir -p /etc/apt/keyrings
curl -fsSL "$GPG_ADDR" | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

printf "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] $DIST_ADDR $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

printf "Installing Docker...\n"
sudo apt-get update -y
sudo apt-get install -y \
  docker-ce \
  docker-ce-cli \
  containerd.io \
  docker-compose-plugin

printf "Verifying the installation of Docker...\n"
sudo docker run hello-world
