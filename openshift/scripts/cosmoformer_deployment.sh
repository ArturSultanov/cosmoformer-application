#!/bin/bash

echo "Creating "cosmoformer-app" namespace and project..."
oc new-project cosmoformer-app

echo "Building deployment with kustomize and applying to the cluster..."
kustomize build ../overlays/dev/ | oc apply -f -
