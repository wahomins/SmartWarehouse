#!/bin/bash
# Relative Distinguished Names (RDNs).
# - CN: Common Name
# - OU: Organizational Unit
# - O: Organization
# - L: Locality
# - S: State Or Province Name
# - C: Country Name
# Read the configuration file
CONFIG_FILE="config.ini"
if [[ -f "$CONFIG_FILE" ]]; then
    source "$CONFIG_FILE"
fi


COMMON_NAME="${COMMON_NAME:-}"
# COMMON_NAME=""

# check which operating system (only macOS or linux)
# Set the common name based on the OS if missing config
# if [[ -z "$COMMON_NAME" ]]; then
#     if [[ "$OSTYPE" =~ ^darwin ]]; then
#         COMMON_NAME=$(scutil --get ComputerName)
#     elif [[ "$OSTYPE" =~ ^linux ]]; then
#         # Get the system's IP address
#         COMMON_NAME=$(hostname -I | awk '{print $1}')
#     fi
# fi

# if [[ "$OSTYPE" =~ ^darwin ]]; then
#     COMMON_NAME=$(scutil --get ComputerName)
# fi

# if [[ "$OSTYPE" =~ ^linux ]]; then
#     COMMON_NAME=$(hostname)
# fi


echo "HOSTNAME IS:- ${COMMON_NAME}"

SUBJECT_CA="/C=KE/ST=Nairobi/L=Nairobi/O=Safaricom/OU=CA/CN=$COMMON_NAME"
SUBJECT_SERVER="/C=KE/ST=Nairobi/L=Nairobi/O=Safaricom/OU=Server/CN=$COMMON_NAME"
SUBJECT_CLIENT="/C=KE/ST=Nairobi/L=Nairobi/O=Safaricom/OU=Client/CN=$COMMON_NAME"

function generate_CA () {
  echo "$SUBJECT_CA"
  openssl req -x509 -nodes -sha256 -newkey rsa:2048 -subj "$SUBJECT_CA" -days 365 -keyout ca.key -out ca.crt
}

function generate_server ()
{
  echo "$SUBJECT_SERVER"
  openssl req -nodes -sha256 -new -subj "$SUBJECT_SERVER" -keyout server.key -out server.csr
  openssl x509 -req -sha256 -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365 -extfile <(printf "subjectAltName=IP:$COMMON_NAME,DNS:localhost")
}

function generate_client ()
{
  echo "$SUBJECT_CLIENT"
  openssl req -new -nodes -sha256 -subj "$SUBJECT_CLIENT" -out client.csr -keyout client.key
  openssl x509 -req -sha256 -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 365
}

function copy_keys_to_certs ()
{
  cp ca.crt ../config/certs/
  cp server.crt ../config/certs/
  cp server.key ../config/certs/
}

generate_CA
generate_server
generate_client
copy_keys_to_certs
