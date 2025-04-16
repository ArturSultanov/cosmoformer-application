import requests
import os

backend_url:str = os.getenv(API_URL, "http://localhost:8000")

def test_root():
    response = requests.get(backend_url)
    assert response.status_code == 200, f"Status code: {response.status_code}"
    data = response.json()
    assert data.get("message") == "Hello World!", f"Failed, got message: {data.get('status')}"

def test_healthcheck():
    response = requests.get(backend_url + "/healthcheck")
    assert response.status_code == 200, f"Status code: {response.status_code}"
    data = response.json()
    assert data.get("message") == "FastAPI backend is up and running!", f"Failed, got message: {data.get('status')}"

def test_readycheck():
    response = requests.get(backend_url + "/readycheck")
    assert response.status_code == 200, f"Status code: {response.status_code}"
    data = response.json()
    assert data.get("message") == "Model is ready.", f"Failed, got message: {data.get('status')}"
