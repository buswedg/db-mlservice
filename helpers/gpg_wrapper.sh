#!/bin/bash

# Script to encrypt or decrypt a file using GPG utility and AES256 cipher.
#
# Usage:
#   gpg_wrapper.sh [-f INPUT_FILE] [-e ENC_MODE]
#
# Arguments:
#   -f INPUT_FILE: The name of the file to encrypt or decrypt.
#   -e ENC_MODE: The encryption mode. Use 'encrypt' or 'decrypt'.
#
# Notes:
#   - The encrypted file is saved as INPUT_FILE.gpg in the same directory as the original file.
#   - The script will prompt the user to enter a passphrase for the encryption key.
#
# Example usage:
#   gpg_wrapper.sh -f dev.env -e encrypt

set -o errexit
set -o nounset
set -o pipefail

while getopts "f:e:" opt; do
  case $opt in
    f)
      INPUT_FILE=$OPTARG
      ;;
    e)
      MODE=$OPTARG
      ;;
    \?)
      printf "\nInvalid option: -$OPTARG"
      exit 1
      ;;
    :)
      printf "\nOption -$OPTARG requires an argument"
      exit 1
      ;;
  esac
done

if [[ -z $INPUT_FILE ]]; then
  printf "\nInput file not specified. Use the -f option."
  exit 1
fi

if [[ -z $MODE ]]; then
  printf "\nEncryption mode not specified. Use the -e option."
  exit 1
fi

function encrypt_file {
  local INPUT_FILE="$1"
  local OUTPUT_FILE="$INPUT_FILE.gpg"
  while true; do
    read -r -s -p "Enter passphrase (min 10 characters): " PASSPHRASE
    if [ ${#PASSPHRASE} -ge 10 ]; then
      break
    else
      echo "Error: Passphrase must be at least 10 characters long"
    fi
  done
  printf "\nEncrypting $INPUT_FILE..."
  gpg --symmetric --cipher-algo AES256 --output "$OUTPUT_FILE" --passphrase "$PASSPHRASE" --batch --yes "$INPUT_FILE"
  if [[ $? -eq 0 ]]; then
    printf "\nDone. Encrypted file: $OUTPUT_FILE"
  else
    printf "\nError: Encryption failed"
    exit 1
  fi
}

function decrypt_file {
  local INPUT_FILE="$1"
  if [[ "$INPUT_FILE" != *.gpg ]]; then
    printf "\nError: $INPUT_FILE is not a GPG file"
    exit 1
  fi
  local OUTPUT_FILE="${INPUT_FILE%.gpg}"
  read -r -s -p "Enter passphrase: " PASSPHRASE
  printf "\nDecrypting $INPUT_FILE..."
  gpg --decrypt --cipher-algo AES256 --output "$OUTPUT_FILE" --passphrase "$PASSPHRASE" --batch --yes "$INPUT_FILE"
  if [[ $? -eq 0 ]]; then
    printf "\nDone. Decrypted file: $OUTPUT_FILE"
  else
    printf "\nError: Decryption failed"
    exit 1
  fi
}

if [[ "$MODE" == "encrypt" ]]; then
  encrypt_file "$INPUT_FILE"
elif [[ "$MODE" == "decrypt" ]]; then
  decrypt_file "$INPUT_FILE"
else
  printf "\nInvalid mode. Use 'encrypt' or 'decrypt'"
  exit 1
fi
