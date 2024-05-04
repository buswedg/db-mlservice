#!/bin/bash

# Script to backup database, encrypting the backup, and uploading it to Azure Blob Storage.
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
#   - DB_NAME: The name of the database to back up.
#   - DB_USERNAME: The username to use when connecting to the database.
#   - DB_PASSWORD: The password to use when connecting to the database.
#   - AZURE_BLOB_ACCOUNT_NAME: The name of the Azure storage account to upload the backup to.
#   - AZURE_BLOB_ACCOUNT_KEY: The access key for the Azure storage account.
#   - DB_CONTAINER_NAME: The name of the Docker container for the database.
#
# Notes:
#   - The script requires Docker, GPG, and the Azure CLI to be installed and configured.
#   - The script will load environment variables from the specified ENV_FILE in the APP_ROOT_DIR directory if they are
#     not already set.
#   - The script will delete backups on Azure storage that are older than $BACKUP_CUTOFF_DAYS days.
#   - You can install Azure CLI using the following: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
#
# Example usage:
#   run_backup_db_to_azure.sh -d /path/to/app/root -e dev.env

set -o errexit
set -o nounset
set -o pipefail

command -v docker >/dev/null 2>&1 || { printf >&2 "docker is required but not installed"; exit 1; }
command -v gpg >/dev/null 2>&1 || { printf >&2 "gpg is required but not installed"; exit 1; }
command -v az >/dev/null 2>&1 || { printf >&2 "az is required but not installed"; exit 1; }

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
      printf >&2 "Invalid option: -%s\n" "$OPTARG"
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
LOG_PATH="$LOG_DIR/backup.log"

AZURE_BLOB_ACCOUNT_NAME=$AZURE_BLOB_ACCOUNT_NAME
AZURE_BLOB_ACCOUNT_KEY=$AZURE_BLOB_ACCOUNT_KEY
AZURE_BLOB_CONTAINER_NAME="backups"

BACKUP_DIR="$APP_ROOT_DIR/backups"
BACKUP_PATH="$BACKUP_DIR/db-backup-$TIMESTAMP.gz"
ENCRYPTED_PATH="$BACKUP_PATH.gpg"

BACKUP_PASSPHRASE="$DB_PASSWORD"
BACKUP_CUTOFF_DAYS=14

mkdir -p "$BACKUP_DIR"

function backup_database() {
  docker exec -i "$DOCKER_DB_CONTAINER" sh -c "pg_dump -F c -U "$DOCKER_DB_USER" "$DOCKER_DB_NAME" > /db.dump" &&
  docker cp "$DOCKER_DB_CONTAINER:/db.dump" "$BACKUP_PATH"
}

function encrypt_backup() {
  gpg --symmetric \
      --cipher-algo AES256 \
      --output "$ENCRYPTED_PATH" \
      --s2k-digest-algo SHA512 \
      --s2k-count 1230456 \
      --passphrase "$BACKUP_PASSPHRASE" \
      --batch --yes \
      "$BACKUP_PATH"
}

function upload_backup() {
  az storage blob upload \
    --account-name "$AZURE_BLOB_ACCOUNT_NAME" \
    --account-key "$AZURE_BLOB_ACCOUNT_KEY" \
    --container-name "$AZURE_BLOB_CONTAINER_NAME" \
    --name "$(basename "$ENCRYPTED_PATH")" \
    --type block \
    --no-progress \
    --file "$ENCRYPTED_PATH"
}

function delete_old_backups() {
  CUTOFF_DATE=$(date -d "$BACKUP_CUTOFF_DAYS days ago" '+%Y-%m-%dT%H:%M:%SZ')
  az storage blob list \
    --account-name "$AZURE_BLOB_ACCOUNT_NAME" \
    --account-key "$AZURE_BLOB_ACCOUNT_KEY" \
    --container-name "$AZURE_BLOB_CONTAINER_NAME" \
    --query "[?properties.creationTime<'$CUTOFF_DATE'].name" \
    --output tsv | xargs -I {} az storage blob delete \
    --account-name "$AZURE_BLOB_ACCOUNT_NAME" \
    --account-key "$AZURE_BLOB_ACCOUNT_KEY" \
    --container-name "$AZURE_BLOB_CONTAINER_NAME" \
    --name {}
}

backup_database
encrypt_backup
upload_backup
delete_old_backups

rm "$BACKUP_PATH" 2>/dev/null
rm "$ENCRYPTED_PATH" 2>/dev/null

printf "Backup successful: %s\n" "$TIMESTAMP" >> "$LOG_PATH"
