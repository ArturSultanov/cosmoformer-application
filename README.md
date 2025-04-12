# Galaxy classification application

This is the backend part of the galaxy classification application for my bachelor thesis

To start application locally use a `docker-compose` or `podman-compose`:
```
podman-compose up --build
```

To deploy app locally into CodeReady Containers (`crc`):
```
crc setup
crc start --cpus 11 --memory 24576
eval $(crc oc-env)
oc login -u kubeadmin https://api.crc.testing:6443
oc new-project cosmoformer-app
kustomize build openshift/overlays/dev/ | oc apply -f -
```
