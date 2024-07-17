#!/bin/sh

chmod +x wait-for-it.sh
chmod +x rebuild.sh

docker-compose -f docker-compose.prod.nginx-proxy.yml --env-file prod.env up
