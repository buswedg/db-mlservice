#!/bin/bash

# Script to load a database backup from Azure Blob Storage and restore it.
#
# Usage:
#   run_restore_db_from_azure.sh [-d APP_ROOT_DIR] [-e ENV_FILE] [-f BACKUP_FILENAME]
#
# Arguments:
#   -d APP_ROOT_DIR: The root directory of the application. Defaults to the current directory if not specified.
#   -e ENV_FILE: The name of the environment file to load from the application root directory (e.g., dev.env, prod.env).
#                Defaults to 'dev.env' if not specified.
#   -f BACKUP_FILENAME: The name of the backup file to restore. If not provided, the latest backup file will be restored.
#
# Required environment variables:
#   - DB_NAME: The name of the database to restore.
#   - DB_USERNAME: The username to use when connecting to the database.
#   - DB_PASSWORD: The password to use when connecting to the database.
#   - AZURE_BLOB_ACCOUNT_NAME: The name of the Azure storage account where the backup is stored.
#   - AZURE_BLOB_ACCOUNT_KEY: The access key for the Azure storage account.
#   - DB_CONTAINER_NAME: The name of the database container.
#
# Notes:
#   - The script requires Docker, GPG, and the Azure CLI to be installed and configured.
#   - The script will load environment variables from the specified ENV_FILE in the APP_ROOT_DIR directory if they are
#     not already set.
#   - The script assumes that the backup file is encrypted with GPG.
#   - You can install Azure CLI using the following: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
#
# Example usage:
#   run_restore_db_from_azure.sh -d /path/to/app/root -e dev.env -f db-backup-2023-06-22-00-00-01.gz.gpg

set -o errexit
set -o nounset
set -o pipefail

command -v docker >/dev/null 2>&1 || { printf >&2 "docker is required but not installed"; exit 1; }
command -v gpg >/dev/null 2>&1 || { printf >&2 "gpg is required but not installed"; exit 1; }
command -v az >/dev/null 2>&1 || { printf >&2 "az is required but not installed"; exit 1; }

APP_ROOT_DIR="."
ENV_FILE="dev.env"
BACKUP_FILENAME=""

while getopts "d:e:f:" opt; do
  case $opt in
    d)
      APP_ROOT_DIR=$OPTARG
      ;;
    e)
      ENV_FILE=$OPTARG
      ;;
    f)
      BACKUP_FILENAME=$OPTARG
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
  DB_PASSWORD
  AZURE_BLOB_ACCOUNT_NAME
  AZURE_BLOB_ACCOUNT_KEY
  DB_CONTAINER_NAME
)

# Load environment variables if not set
if [ -f "$ENV_FILE_PATH" ]; then
  while IFS='=' read -r var_name var_value || [ -n "$var_name" ]; do
    if [[ ! $var_name =~ ^# && -n $var_value && " ${REQUIRED_VARS[@]} " =~ " ${var_name} " ]]; then
      var_value=$(sed -e "s/^\(['\"]\)\(.*\)\1\$/\2/" <<< "$var_value")
      var_value=${var_value%%$'\r'}
      export "$var_name=$var_value"
    fi
  done < "$ENV_FILE_PATH"
else
  printf "Environment file not found: %s\n" "$ENV_FILE_PATH" >&2
  exit 1
fi

# Check if all required variables are set
for var in "${REQUIRED_VARS[@]}"; do
  if [ -z "${!var}" ]; then
    printf "Error: Required environment variable $var is not set"
    exit 1
  fi
done

DOCKER_DB_CONTAINER=$DB_CONTAINER_NAME
DOCKER_DB_NAME=$DB_NAME
DOCKER_DB_USER=$DB_USERNAME

TIMESTAMP=$(date +"%Y-%m-%d-%H-%M-%S")

LOG_DIR="$APP_ROOT_DIR/logs"
LOG_PATH="$LOG_DIR/restore.log"

AZURE_BLOB_ACCOUNT_NAME=$AZURE_BLOB_ACCOUNT_NAME
AZURE_BLOB_ACCOUNT_KEY=$AZURE_BLOB_ACCOUNT_KEY
AZURE_BLOB_CONTAINER_NAME="backups"

if [[ -z "$BACKUP_FILENAME" ]]; then
  BACKUP_FILENAME=$(
    az storage blob list \
      --account-name "$AZURE_BLOB_ACCOUNT_NAME" \
      --account-key "$AZURE_BLOB_ACCOUNT_KEY" \
      --container-name "$AZURE_BLOB_CONTAINER_NAME" \
      --query "sort_by([], &properties.creationTime)[-1].name" \
      --output tsv
  )
  printf "$BACKUP_FILENAME"
fi

BACKUP_DIR="$APP_ROOT_DIR/backups"
RESTORE_PATH="$BACKUP_DIR/$BACKUP_FILENAME"
DECRYPTED_PATH="$RESTORE_PATH.decrypted"

mkdir -p "$BACKUP_DIR"

function download_backup() {
  az storage blob download \
    --account-name "$AZURE_BLOB_ACCOUNT_NAME" \
    --account-key "$AZURE_BLOB_ACCOUNT_KEY" \
    --container-name "$AZURE_BLOB_CONTAINER_NAME" \
    --name "$BACKUP_FILENAME" \
    --file "$RESTORE_PATH" \
    --no-progress
}

function decrypt_backup() {
  gpg --decrypt \
      --cipher-algo AES256 \
      --output "$DECRYPTED_PATH" \
      --s2k-digest-algo SHA512 \
      --s2k-count 1230456 \
      --passphrase "$DB_PASSWORD" \
      --batch --yes \
      "$RESTORE_PATH"
}

function restore_database() {
  docker cp "$DECRYPTED_PATH" "$DOCKER_DB_CONTAINER:/db.dump"
  docker exec -i "$DOCKER_DB_CONTAINER" sh -c "pg_restore -d $DOCKER_DB_NAME -U $DOCKER_DB_USER /db.dump --clean --no-owner"
}

download_backup
decrypt_backup
restore_database

rm "$RESTORE_PATH" 2>/dev/null
rm "$DECRYPTED_PATH" 2>/dev/null

printf "Restore successful: %s\n" "$TIMESTAMP" >> "$LOG_PATH"
