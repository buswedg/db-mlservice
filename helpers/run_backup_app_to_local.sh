#!/bin/bash

# Script to backup key app data (db, media and logs) to local folder.
#
# Usage:
#   run_backup_db_to_azure.sh [-d APP_ROOT_DIR] [-e ENV_FILE]
#
# Arguments:
#   -d APP_ROOT_DIR: The root directory of the application. Defaults to the current directory if not specified.
#   -e ENV_FILE: The name of the environment file to load from the application root directory (e.g. dev.env, prod.env).
#                Defaults to 'dev.env' if not specified.
#
# Required environment variables:
#   - DB_NAME: The name of the database to backup
#   - DB_USERNAME: The username to use when connecting to the database
#
# Notes:
#   - The script will load environment variables from the specified ENV_FILE in the APP_ROOT_DIR directory if they are
#     not already set.
#
# Example usage:
#   run_backup_app_to_local.sh -d /path/to/app/root -e dev.env

set -o errexit
set -o nounset
set -o pipefail

command -v docker >/dev/null 2>&1 || { printf >&2 "docker is required but not installed"; exit 1; }

APP_ROOT_DIR="."
ENV_FILE="dev.env"

while getopts "d:e:" opt; do
  case $opt in
    d)
      APP_ROOT_DIR=$OPTARG
      ;;
    e)
      ENV_FILE=$OPTARG
      ;;
    \?)
      printf >&2 "Invalid option: -$OPTARG\n"
      exit 1
      ;;
  esac
done

ENV_FILE_PATH="$APP_ROOT_DIR/$ENV_FILE"

REQUIRED_VARS=(
  DB_NAME
  DB_USERNAME
  DJANGO_CONTAINER_NAME
  DB_CONTAINER_NAME
)

# Load environment variables if not set
while IFS="=" read -r var_name var_value; do
  if [[ " ${REQUIRED_VARS[@]} " =~ " ${var_name} " ]] && [[ -z "${!var_name:-}" ]]; then
    export "$var_name=${var_value}"
  fi
done < "$ENV_FILE_PATH"

DOCKER_APP_CONTAINER=$DJANGO_CONTAINER_NAME
DOCKER_DB_CONTAINER=$DB_CONTAINER_NAME
DOCKER_DB_NAME=$DB_NAME
DOCKER_DB_USER=$DB_USERNAME

TIMESTAMP=$(date +"%Y-%m-%d-%H-%M-%S")

LOG_DIR="$APP_ROOT_DIR/logs"
LOG_PATH="$LOG_DIR/backup.log"
BACKUP_DIR="$APP_ROOT_DIR/backups/$TIMESTAMP"
BACKUP_PATH="$BACKUP_DIR/db.dump"

mkdir -p "$BACKUP_DIR"

# Dump database into file and copy to host
docker exec -u 0 -i $DOCKER_DB_CONTAINER sh -c "pg_dump -F c -U $DOCKER_DB_USER $DOCKER_DB_NAME > /db.dump" && \
docker cp $DOCKER_DB_CONTAINER:/db.dump $BACKUP_PATH

if [ $? -ne 0 ]; then
  printf "Error dumping database\n" >&2
  exit 1
fi

# Backup app media and logs
docker cp $DOCKER_APP_CONTAINER:/usr/src/app/media $BACKUP_DIR/media && \
docker cp $DOCKER_APP_CONTAINER:/usr/src/app/logs $BACKUP_DIR/logs

if [ $? -ne 0 ]; then
  printf "Error backing up media and logs\n" >&2
  exit 1
fi

printf "Backup successful: %s\n" "$TIMESTAMP" >> "$LOG_PATH"
