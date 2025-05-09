# Galaxy classification application

- [Galaxy classification application](#galaxy-classification-application)
  - [Introduction](#introduction)
  - [Application Overview](#application-overview)
    - [Backend](#backend)
    - [Frontend](#frontend)
    - [Openshift](#openshift)
  - [Local deployment](#local-deployment)
    - [Docker-compose deployment](#docker-compose-deployment)
    - [CRC deployment](#crc-deployment)
  - [Tests](#tests)
    - [API tests](#api-tests)
    - [Kustomize tests](#kustomize-tests)
    - [Performance tests](#performance-tests)
    - [Galaxy Zoo 2](#galaxy-zoo-2)
  - [Links:](#links)

## Introduction

This repository "Galaxy classification application" contains the code of application that can classify galaxy images, which is the part of my Bachelor thesis at Brno Technical University (BUT).

**Thesis title**: AI-Powered Web Application for Galaxy Morphology Classification on Red Hat OpenShift  
**Acad. year**: 2024/2025  
**Department**: Department of Intelligent Systems  
**Type of thesis**: Bachelor's Thesis  
**Language of thesis**: en  
**Thesis focus**: Artificial Intelligence  
**Supervisor**: Mgr. Kamil Malinka, Ph.D.  
**Reviewer**: Ing. Milan Šalko  
**Consultant**: Forde Kieran, Ph.D.  

**Electronic source citation (english):**
```
SULTANOV, Artur. AI-Powered Web Application for Galaxy Morphology Classification on Red Hat OpenShift. Online, bachelor's Thesis. Kamil MALINKA (supervisor). Brno: Brno University of Technology, Faculty of Information Technology, 2025. Available at: https://www.vut.cz/en/students/final-thesis/detail/164309. [accessed 2025-04-15].
```
---

## Application Overview

The main idea was to create a web application, which uses ViT-based model to predict galaxy morphological class based on images of galaxy.

![Web UI](<frontend_ui.png>)

The application is consist of the follwing parts:

### Backend

The whole backend is written in `Python` language, which is wide-used for ML purposes. For model loading and inference I used `PyTorch` library, that was used for model training as well. This approach ensure a consistency while using AI model, that was written using PyTorch, and reduce the complexity of development.  

The heart of the application is `CosmoFormer`, the model that is based on a `Crossformer` architecture and trained by me on `Galaxy Zoo 2` dataset (Hugging Face: [artursultanov/cosmoformer-model](https://huggingface.co/artursultanov/cosmoformer-model)). This model was optimize to consume as less resources as possible while delivering dissent inference CPU performance.

Backend provide a (REST) API for communication with frontend. For that purpose I chose the `FastAPI` framework. `FastAPI` is a modern, high-performance, web framework for building APIs with Python based on standard Python type hints. `Uvicorn` was used as web server. `Uvicorn` implements a multi-process model with one main process, which is responsible for managing a pool of worker processes and distributing incoming HTTP requests to them.

### Frontend

The used-end interface was be created using `JavaScript` and `React` library. `NGINX` is web server that keeps static and also works as reverse proxy, redirecting request to backend API.

### Openshift

The application was design to be easily deployable into modern hybrid-cloud cloud platforms such as Red Hat Openshift Container Platform. 

The Docker images have been build for both Backend and Frontend parts. They can be found at [Quay.io](https://quay.io/user/rhit_asultano/?tab=settings):
- [rhit_asultano/cosmoformer-backend](https://quay.io/repository/rhit_asultano/cosmoformer-backend)
- [rhit_asultano/cosmoformer-frontend](https://quay.io/repository/rhit_asultano/cosmoformer-frontend)

The needed resource declarations are added to `openshift` folder. That includes:
- Backend Deployment: `cosmoformer-backend-deployment`
- Backend HorizontalPodAutoscaler: `cosmoformer-backend-hpa`
- Backend Service: `cosmoformer-backend-service`
- Frontend Deployment: `cosmoformer-frontend-deployment`
- Frontend HorizontalPodAutoscaler: `cosmoformer-frontend-hpa`
- Frontend Service: `cosmoformer-frontend-service`
- Frontend Route: `cosmoformer-frontend-route`
- **Example** Project: `cosmoformer-app` (commented, not used)
- ResourceQuota: `cosmoformer-rq`

The process of deployment was automated by using [cosmoformer_deployment.sh](openshift/cosmoformer_deployment.sh) script, which can be easily integrated into CI/CD pipeline.

## Local deployment

There are two way how you can test the application locally: `docker-compose` or `crc`

### Docker-compose deployment

To start application locally use a `docker-compose` or `podman-compose` use following command:

```bash
podman-compose up --build
```

It will build containers and run backend container at `http://localhost:8000/` and frontend container at `http://localhost:8080/`.

### CRC deployment

CRC brings a minimal OpenShift Container Platform 4 cluster to your local computer. This runtime provides minimal environments for development and testing purposes. For deployment use following steps to deploy application locally:

1. Start CodeReady Containers (`crc`) using [crc_startup.sh](openshift/crc_startup.sh) script:
```bash
./crc_startup.sh 
```

The output should look as follows:

```bash
Started the OpenShift cluster.

The server is accessible via web console at:
  https://console-openshift-console.apps-crc.testing

Log in as administrator:
  Username: kubeadmin
  Password: sXg3P-TzKWQ-kLqwg-dD3Vc

Log in as user:
  Username: developer
  Password: developer

Use the 'oc' command line interface:
  $ eval $(crc oc-env)
  $ oc login -u developer https://api.crc.testing:6443

CRC Console URL:
https://console-openshift-console.apps-crc.testing

CRC Console credentials:
To login as a regular user, run 'oc login -u developer -p developer https://api.crc.testing:6443'.
To login as an admin, run 'oc login -u kubeadmin -p sXg3P-TzKWQ-kLqwg-dD3Vc https://api.crc.testing:6443'
```

2. Deploy needed Openshift resouces using [cosmoformer_deployment.sh](openshift/cosmoformer_deployment.sh) script:
```bash
./cosmoformer_deployment.sh
```

The output should look as follows:

```bash
Creating cosmoformer-app namespace and project...
Now using project "cosmoformer-app" on server "https://api.crc.testing:6443".

You can add applications to this project with the 'new-app' command. For example, try:

    oc new-app rails-postgresql-example

to build a new example application in Ruby. Or use kubectl to deploy a simple Kubernetes application:

    kubectl create deployment hello-node --image=registry.k8s.io/e2e-test-images/agnhost:2.43 -- /agnhost serve-hostname

Building deployment with kustomize and applying to the cluster...
resourcequota/cosmoformer-rq created
service/cosmoformer-backend-service created
service/cosmoformer-frontend-service created
deployment.apps/cosmoformer-backend-deployment created
deployment.apps/cosmoformer-frontend-deployment created
horizontalpodautoscaler.autoscaling/cosmoformer-backend-hpa created
horizontalpodautoscaler.autoscaling/cosmoformer-frontend-hpa created
route.route.openshift.io/cosmoformer-frontend-route created
```

## Tests

Tests locates in [tests](tests) folder. Each subfolder contains the specific sets of tests to validate key apllication parts.

### API tests

The [tests/api](tests/api) folder contains tests to validate backend API functionality. It's needed to specify `API_URL` environment variable that points to backend API. For example, `export API_URL="http://localhost:8000"`.

1. **[test_api.py](tests/api/test_api.py)** - test if main backend endpoints work as expected.
2. **[test_inference.py](tests/api/test_inference.py)** - test if AI model is load and can predict the galaxy class on galaxy image.

**Prerequisites:**
- Running backend. For example, the docker container spinned up using `podman-compose up --build`.

To run the tests:

```bash
pytest tests/api/
```

### Kustomize tests

The [tests/kustomize](tests/kustomize) folder contains tests to validate the Kustomize overlays for the OpenShift deployment.

1. **[test_kustomize_build.sh](tests/kustomize/test_kustomize_build.sh)** – builds the overlay (`openshift/overlays/dev`) with `kustomize build` and writes the rendered manifest to `/tmp/cosmoformer_openshift.yaml`. It also prints a summary of generated resource kinds and the full YAML to stdout.  
2. **[test_kustomize_dry_run.sh](tests/kustomize/test_kustomize_dry_run.sh)** – takes the rendered manifest and runs `oc apply --dry-run=client` to ensure the YAML is syntactically valid for the OpenShift API (nothing is actually created). It exits with an error if the manifest is missing or the dry‑run fails.

**Prerequisites:**  
- `kustomize` CLI in `$PATH`  
- `oc` CLI logged in (any context is fine because the test uses `--dry-run=client`)  

To run the tests:

```bash
tests/kustomize/test_kustomize_build.sh
tests/kustomize/test_kustomize_dry_run.sh
```

### Performance tests

The [tests/performance](tests/performance) folder contains a **k6** test that measures the throughput and latency of the `/inference` endpoint. This also is good way to check if [HorizontalPodAutoscaler's](#openshift) (which are used in cluster) work as expected. The test executes a “ramping‑vus” scenario of performance and stress tests. This scenario starts with increasing the  virtual users (VUs) from 0 to 5 in the first 10 seconds, keeps 5 users active for 280 seconds, then ramps back down to 0 during the final 10 seconds.The delay between requests of one user is 5 seconds, which simulates the time needed for a real person to upload an image. The entire testing time is 5 minutes. 

1. **[run_k6_test.sh](tests/performance/run_k6_test.sh)** – helper script that  
   * picks a target URL automatically (prefers the OpenShift Route and falls back to `http://localhost:8000/inference`),  
   * exports `TARGET_URL` and `IMAGES_JSON` environment variables, and  
   * runs [performance_test.js](tests/performance/performance_test.js) test.

2. **[performance_test.js](tests/performance/performance_test.js)** – a k6 script that executes a “ramping‑vus” scenario to load-test app, checks only 5 % of requests fail and checl the latencies stay under 1 s for 90% of requests and 2 s for 95% of requests.

**Prerequisites**  
- **k6** CLI in `$PATH` (`brew install k6` or `dnf install k6`)  
- The sample images listed in `tests/images/images.json`  
- Optional: `curl` in the helper script’s path

To execute the performance test:

```bash
tests/performance/run_k6_test.sh
```
The output should look as follows:

```
TARGET_URL not set. Checking route crc and container...
Using TARGET_URL: http://cosmoformer-frontend-route-cosmoformer-app.apps-crc.testing/api/inference
Running k6 test ...

         /\      Grafana   /‾‾/  
    /\  /  \     |\  __   /  /   
   /  \/    \    | |/ /  /   ‾‾\ 
  /          \   |   (  |  (‾)  |
 / __________ \  |_|\_\  \_____/ 

     execution: local
        script: performance_test.js
        output: -

     scenarios: (100.00%) 1 scenario, 5 max VUs, 45s max duration (incl. graceful stop):
              * performace_test: Up to 5 looping VUs for 40s over 3 stages (gracefulRampDown: 30s, exec: performTest, gracefulStop: 5s)

INFO[0003] Response for 33_test.jpg: status 200, body: {"predicted_class":"Smooth Round"}  source=console
  .
  .
  .

  █ THRESHOLDS 

    http_req_duration
    ✗ 'p(90)<1000' p(90)=30s
    ✗ 'p(95)<2000' p(95)=30s

    http_req_failed
    ✗ 'rate<0.05' rate=31.52%


  █ TOTAL RESULTS 

    checks_total.......................: 184    0.603278/s
    checks_succeeded...................: 64.13% 118 out of 184
    checks_failed......................: 35.86% 66 out of 184

    ✗ status was 200
      ↳  68% — ✓ 63 / ✗ 29
    ✗ response time < 2s
      ↳  59% — ✓ 55 / ✗ 37

    HTTP
    http_req_duration.......................................................: avg=10.82s min=39.52ms med=273.9ms  max=30.01s p(90)=30s   p(95)=30s  
      { expected_response:true }............................................: avg=1.99s  min=39.52ms med=176.31ms max=22.08s p(90)=9.73s p(95)=14.2s
    http_req_failed.........................................................: 31.52% 29 out of 92
    http_reqs...............................................................: 92     0.301639/s

    EXECUTION
    iteration_duration......................................................: avg=15.4s  min=5.04s   med=5.27s    max=35.01s p(90)=35s   p(95)=35s  
    iterations..............................................................: 90     0.295082/s
    vus.....................................................................: 4      min=0        max=5
    vus_max.................................................................: 5      min=5        max=5

    NETWORK
    data_received...........................................................: 40 kB  130 B/s
    data_sent...............................................................: 1.3 MB 4.4 kB/s




running (5m05.0s), 0/5 VUs, 90 complete and 4 interrupted iterations
performace_test ✓ [======================================] 4/5 VUs  5m0s
ERRO[0306] thresholds on metrics 'http_req_duration, http_req_failed' have been crossed 
```

### Galaxy Zoo 2

    @article{10.1093/mnras/stt1458,
    author = {Willett, Kyle W. and Lintott, Chris J. and Bamford, Steven P. and Masters, Karen L. and Simmons, Brooke D. and Casteels, Kevin R. V. and Edmondson, Edward M. and Fortson, Lucy F. and Kaviraj, Sugata and Keel, William C. and Melvin, Thomas and Nichol, Robert C. and Raddick, M. Jordan and Schawinski, Kevin and Simpson, Robert J. and Skibba, Ramin A. and Smith, Arfon M. and Thomas, Daniel},
    title = "{Galaxy Zoo 2: detailed morphological classifications for 304 122 galaxies from the Sloan Digital Sky Survey}",
    journal = {Monthly Notices of the Royal Astronomical Society},
    volume = {435},
    number = {4},
    pages = {2835-2860},
    year = {2013},
    month = {09},
    issn = {0035-8711},
    doi = {10.1093/mnras/stt1458},
    }

## Links:
1. Galaxy classification application: https://github.com/ArturSultanov/cosmoformer-application
2. CosmoFormer model: https://github.com/ArturSultanov/cosmoformer-model
3. CosmoFormer dataset: https://github.com/ArturSultanov/cosmoformer-dataset
4. CosmoFormer dataset (no pre-downloaded images): https://github.com/ArturSultanov/cosmoformer-dataset-no-images