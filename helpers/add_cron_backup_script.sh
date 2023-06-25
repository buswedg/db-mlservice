#!/bin/bash

# Script for automatically scheduling a backup task using cron.

# Usage:
#   add_cron_backup_script.sh [-d APP_ROOT_DIR] [-s SCRIPT_FILE] [-e ENV_FILE]
#
# Arguments:
#   -d APP_ROOT_DIR: The root directory of the application.
#   -s SCRIPT_FILE: The name of the backup script to run from the helpers folder in the application root directory.
#                   Defaults to 'run_backup_db_to_azure.sh' if not specified.
#   -e ENV_FILE: The name of the environment file to load from the application root directory (e.g. dev.env, prod.env).
#                Defaults to 'dev.env' if not specified.
#
# Description:
#   This script adds a cron entry to automatically schedule a backup task. It executes the backup script at a specified
#   time interval and redirects the output to a log file.
#
# Example usage:
#   add_cron_backup_script.sh -d /path/to/app/root -s run_backup_db_to_azure.sh -e dev.env

set -o errexit
set -o nounset
set -o pipefail

APP_ROOT_DIR=""
SCRIPT_FILE="run_backup_db_to_azure.sh"
ENV_FILE="dev.env"

while getopts "d:s:e:" opt; do
  case $opt in
    d)
      APP_ROOT_DIR=$OPTARG
      ;;
    s)
      SCRIPT_FILE=$OPTARG
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

if [ -z $APP_ROOT_DIR ]; then
  printf >&2 "Missing required option: -d APP_ROOT_DIR\n"
  exit 1
fi

SCHEDULE="0 */8 * * *"
USER="root"
SCRIPT_PATH="$APP_ROOT_DIR/helpers/$SCRIPT_FILE"
LOG_DIR="$APP_ROOT_DIR/logs"
LOG_PATH="$LOG_DIR/backup.log"
CRON_DIR="/etc/cron.d"
CRON_FILE="schedule"
CRON_PATH="$CRON_DIR/$CRON_FILE"

sudo mkdir -p $CRON_DIR
sudo touch $CRON_PATH
sudo mkdir -p $LOG_DIR
sudo touch $LOG_PATH
sudo chmod 644 $LOG_PATH
sudo chmod 644 $CRON_PATH
sudo chmod +x $SCRIPT_PATH

CRON_SCHEDULE="$SCHEDULE $USER /bin/bash -c \"$SCRIPT_PATH -d $APP_ROOT_DIR -e $ENV_FILE >> $LOG_PATH 2>&1\""

if ! sudo grep -qF $SCRIPT_PATH $CRON_PATH; then
    echo "$CRON_SCHEDULE" | sudo tee -a $CRON_PATH >/dev/null
fi

sudo service cron reload
