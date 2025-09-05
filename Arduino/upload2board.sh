#!/bin/bash
set -e

# Those defaults are needed for the built package
BUILD_DIR=${1:-/usr/share/spear/firmware/}
DEFAULT_FQBN=${2:-arduino:avr:nano:cpu=atmega328old}

AC_RESULT=$(arduino-cli board list | grep "Serial Port (USB)" | sed "s/Serial Port (USB)//g")

PORT=$(echo "${AC_RESULT}" | awk '{print $1}')
FQBN=$(echo "${AC_RESULT}" | awk '{print $3}')

if [[ "${FQBN}" == "Unknown" || -z "${FQBN}" ]]; then
  echo "Unknown Port detected, using default = ${DEFAULT_FQBN}"
  FQBN=${DEFAULT_FQBN}
fi

echo "Uploading code to board ${FQBN} on port ${PORT}"
arduino-cli upload -v -p "${PORT}" -b "${FQBN}" --input-dir "${BUILD_DIR}"
echo "Upload successful!"
