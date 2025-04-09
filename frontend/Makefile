IMAGE_NAME := cosmoformer-frontend-image
CONTAINER_NAME := cosmoformer-frontend-container
LPORT := 8080
CPORT := 8080
.PHONY: build run stop logs shell clean

build:
	@echo "Building image $(IMAGE_NAME)..."
	docker build -t $(IMAGE_NAME) .

run:
	@echo "Running container $(CONTAINER_NAME)..."
	docker run --name $(CONTAINER_NAME) -p $(LPORT):$(CPORT) -d $(IMAGE_NAME)

stop:
	@echo "Stopping container $(CONTAINER_NAME)..."
	docker stop $(CONTAINER_NAME)

logs:
	@echo "Showing logs for container $(CONTAINER_NAME)..."
	docker logs -f $(CONTAINER_NAME)

shell:
	@echo "Opening shell in container $(CONTAINER_NAME)..."
	docker exec -it $(CONTAINER_NAME) bash

clean:
	@echo "Removing container and image..."
	-docker rm $(CONTAINER_NAME) || true
	-docker rmi $(IMAGE_NAME) || true
