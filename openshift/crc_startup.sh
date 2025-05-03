#!/bin/bash
set -e

echo "Setting CRC preset to openshift..."
crc config set preset openshift
crc config set enable-cluster-monitoring true

echo "Running crc setup..."
crc setup

echo "Starting CRC cluster with 24576 MB of memory..."
crc start --cpus $(nproc --ignore=1) --memory 24576
eval "$(crc oc-env)"

echo

echo "CRC Console URL:"
crc console --url

echo

echo "CRC Console credentials:"
crc console --credentials
