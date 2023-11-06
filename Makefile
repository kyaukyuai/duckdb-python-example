.DEFAULT_GOAL := run

IMAGE_NAME := kyaukyuai/duckdb-python
LATEST_IMAGE_NAME := kyaukyuai/duckdb-python:latest

build:
	@docker build -t $(IMAGE_NAME) -t $(LATEST_IMAGE_NAME) .

run:
	@docker run --rm -it $(IMAGE_NAME) /bin/bash

push: build
	docker push $(IMAGE_NAME)
	docker push $(LATEST_IMAGE_NAME)
