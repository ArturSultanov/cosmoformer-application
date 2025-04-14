#!/bin/bash
set -e

if [ ! -f /tmp/cosmoformer_openshift.yaml ]; then
  echo "File '/tmp/cosmoformer_openshift.yaml' does not exist. Please, run test_kustomize_build.sh first."
  exit 1
fi

echo "Applying manifest in dry-run mode..."
oc apply --dry-run=client -f /tmp/cosmoformer_openshift.yaml
