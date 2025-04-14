#!/bin/bash
set -e

echo "Building OpenShift manifests from overlays/dev..."
kustomize build ../openshift/overlays/dev/ > /tmp/cosmoformer_openshift.yaml

echo

echo "Builded components:"
grep "^kind:" /tmp/cosmoformer_openshift.yaml

echo

echo "Builded manifest:"
cat /tmp/cosmoformer_openshift.yaml
