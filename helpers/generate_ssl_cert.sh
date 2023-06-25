#!/bin/bash

set -e

sudo apt-get update -y
sudo apt-get install -y openssl

mkdir -p certs
cd certs

# generate private key and certificate signing request
openssl genrsa -aes256 -out server.key 2048
read -p "Enter the common name for the certificate (e.g. myserver.example.com): " common_name
openssl req -new -key server.key -out server.csr -subj "/CN=${common_name}"

# sign certificate with private key and generate self-signed certificate
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

echo "Certificate information:"
openssl x509 -in server.crt -noout -text

chmod 400 server.key

tar -czvf certs.tar.gz *
#tar -xzvf certs.tar.gz