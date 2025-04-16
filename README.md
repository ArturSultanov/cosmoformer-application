# Galaxy classification application

- [Galaxy classification application](#galaxy-classification-application)
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

The [tests/performance](tests/performance) folder contains a **k6** test that measures the throughput and latency of the `/inference` endpoint. This also is good way to check if [HorizontalPodAutoscaler's](#openshift) (which are used in cluster) work as expected.

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
INFO[0004] Response for 24_test.jpg: status 200, body: {"predicted_class":"Unbarred Spiral"}  source=console
INFO[0022] Response for 58_test.jpg: status 200, body: {"predicted_class":"Smooth Inbetween"}  source=console
INFO[0035] Response for 41_test.jpg: status 200, body: {"predicted_class":"Smooth Inbetween"}  source=console
INFO[0036] Response for 84_test.jpg: status 504, body: <html><body><h1>504 Gateway Time-out</h1>
The server didn't respond in time.
</body></html>  source=console
INFO[0039] Response for 23_test.jpg: status 504, body: <html><body><h1>504 Gateway Time-out</h1>
The server didn't respond in time.
</body></html>  source=console
INFO[0042] Response for 90_test.jpg: status 504, body: <html><body><h1>504 Gateway Time-out</h1>
The server didn't respond in time.
</body></html>  source=console


  █ THRESHOLDS 

    http_req_duration
    ✗ 'p(90)<1000' p(90)=30s
    ✗ 'p(95)<2000' p(95)=30s

    http_req_failed
    ✗ 'rate<0.05' rate=42.85%


  █ TOTAL RESULTS 

    checks_total.......................: 14     0.311108/s
    checks_succeeded...................: 42.85% 6 out of 14
    checks_failed......................: 57.14% 8 out of 14

    ✗ status was 200
      ↳  57% — ✓ 4 / ✗ 3
    ✗ response time < 2s
      ↳  28% — ✓ 2 / ✗ 5

    HTTP
    http_req_duration.......................................................: avg=17.06s min=414.49ms med=16.8s max=30s    p(90)=30s    p(95)=30s   
      { expected_response:true }............................................: avg=7.35s  min=414.49ms med=6.1s  max=16.8s  p(90)=15.28s p(95)=16.04s
    http_req_failed.........................................................: 42.85% 3 out of 7
    http_reqs...............................................................: 7      0.155554/s

    EXECUTION
    iteration_duration......................................................: avg=18.06s min=1.41s    med=17.8s max=31.01s p(90)=31.01s p(95)=31.01s
    iterations..............................................................: 7      0.155554/s
    vus.....................................................................: 3      min=0      max=5
    vus_max.................................................................: 5      min=5      max=5

    NETWORK
    data_received...........................................................: 16 kB  353 B/s
    data_sent...............................................................: 148 kB 3.3 kB/s




running (45.0s), 0/5 VUs, 7 complete and 3 interrupted iterations
performace_test ✓ [======================================] 0/5 VUs  40s
ERRO[0045] thresholds on metrics 'http_req_duration, http_req_failed' have been crossed 
```
