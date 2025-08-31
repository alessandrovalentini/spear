#!/bin/bash
set -e

BUILD_DIR=$1
DEFAULT_FQBN=$2

AC_RESULT=$(arduino-cli board list | grep "Serial Port (USB)" | sed "s/Serial Port (USB)//g")

PORT=$(echo ${AC_RESULT} | awk '{print $1}')
FQBN=$(echo ${AC_RESULT} | awk '{print $3}')

if [[ "${FQBN}" == "Unknown" ]]; then
  echo "Unknown Port detected, using default = ${DEFAULT_FQBN}"
  FQBN=${DEFAULT_FQBN}
fi

echo "Uploading code to board ${FQBN} on port ${PORT}"
arduino-cli upload -v -p "${PORT}" -b "${FQBN}" --input-dir ${BUILD_DIR}
echo "Upload successful!"