# Galaxy classification application

- [Galaxy classification application](#galaxy-classification-application)
  - [Application Overview](#application-overview)
    - [Backend:](#backend)
    - [Frontend](#frontend)
    - [Openshift](#openshift)
  - [Openshift deployment](#openshift-deployment)
  - [Local deployment](#local-deployment)
    - [Docker-compose deployment](#docker-compose-deployment)
    - [CRC deployment](#crc-deployment)
  - [Tests](#tests)


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

The application is consist of 2 main parts: backend and frontend.

### Backend: 

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

The process of deployment was automated by using `cosmoformer_deployment.sh` script, which can be easily integrated into CI/CD pipeline (see [Openshift deployment](#openshift-deployment)).

## Openshift deployment 

## Local deployment

There are two way how you can test the application locally: `docker-compose` and `crc`

### Docker-compose deployment

To start application locally use a `docker-compose` or `podman-compose` use following command:

```
podman-compose up --build
```

It will build containers and run backend container at `http://localhost:8000/` and frontend container at `http://localhost:8080/`.

### CRC deployment

CRC brings a minimal OpenShift Container Platform 4 cluster to your local computer. This runtime provides minimal environments for development and testing purposes. For deployment use following steps:

To deploy app locally into CodeReady Containers (`crc`):
```
crc setup
crc start --cpus 11 --memory 24576
eval $(crc oc-env)
oc login -u kubeadmin https://api.crc.testing:6443
oc new-project cosmoformer-app
kustomize build openshift/overlays/dev/ | oc apply -f -
```


./crc_startup.sh 
```
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

./cosmoformer_deployment.sh
```
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

```
./run_k6_test.sh 
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

