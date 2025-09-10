#!/bin/bash
set -e

# Those defaults are needed for the built package
BUILD_DIR=${1:-/usr/share/spear/firmware/}
CONF_FILE="/etc/avrdude.conf"
MCU_TYPE="atmega328p"
PORT=$(ls /dev/ttyUSB* | head -n1)
BAUD_RATE=${2:-"57600"}
SKETCH_NAME="multi_ac_current_measure.ino"
SKETCH_PATH="$BUILD_DIR/$SKETCH_NAME"
PROGRAMMER_TYPE="arduino"

if [ -z "$PORT" ]; then
  echo "Unable to find an arduino connected!" >&2
  exit 1
fi


echo "Uploading code to board on port ${PORT}"
avrdude -C"${CONF_FILE}" -v -p${MCU_TYPE} -c"${PROGRAMMER_TYPE}" -P"${PORT}" -b"${BAUD_RATE}" -D -U"flash:w:${SKETCH_PATH}.hex:i"
echo "Upload successful!"
