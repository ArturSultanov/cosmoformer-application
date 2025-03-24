IMAGE_NAME := cosmoformer-image
CONTAINER_NAME := cosmoformer-container
LPORT := 8000
CPORT := 8000
.PHONY: build run stop logs shell clean

build:
	@echo "Building image $(IMAGE_NAME)..."
	docker build -t $(IMAGE_NAME) .

run:
	@echo "Running container $(CONTAINER_NAME)..."
	docker run --rm --name $(CONTAINER_NAME) -p $(LPORT):$(CPORT) -d -v $(PWD):/app:Z $(IMAGE_NAME)

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
