#!/bin/bash

set -e

sudo apt-get update -y

printf "Installing s3cmd...\n"
sudo apt-get install s3cmd -y

printf "Configuring s3cmd...\n"
s3cmd --configure

printf "Listing buckets...\n"
s3cmd ls