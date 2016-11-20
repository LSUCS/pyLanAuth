#!/bin/bash
# Install upstart scripts
readonly SCRIPT_DIR=$(dirname $0)

if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root"
    exit 1
fi

echo "Copying scripts to /etc/init.d:"
echo "$(ls $SCRIPT_DIR/*.conf)"

cp $SCRIPT_DIR/*.conf /etc/init

echo "Complete"
