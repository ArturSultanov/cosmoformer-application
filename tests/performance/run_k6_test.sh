#!/usr/bin/env bash
set -e

if [ ! -f "../images/images.json" ]; then
  echo "Error: ../images/images.json does not exist!"
  exit 1
fi

CRC_URL="http://cosmoformer-frontend-route-cosmoformer-app.apps-crc.testing/api/inference"
CONTAINER_URL="http://localhost:8000/inference"

check_url() {
  local url="$1"
  curl --insecure --head --silent --fail "$url" > /dev/null
}

if [ -z "$TARGET_URL" ]; then
  echo "TARGET_URL not set. Checking route crc and container..."

  if check_url "$CRC_URL"; then
    echo "Using TARGET_URL: $CRC_URL"
    export TARGET_URL="$CRC_URL"
  elif check_url "$CONTAINER_URL"; then
    echo "Using TARGET_URL: $CONTAINER_URL"
    export TARGET_URL="$CONTAINER_URL"
  else
    echo "Error: TARGET_URL wasn't set."
    exit 1
  fi
else
  echo "TARGET_URL: $TARGET_URL"
fi

export IMAGES_JSON="$(cat "../images/images.json")"

echo "Running k6 test ..."
k6 run --insecure-skip-tls-verify performance_test.js
