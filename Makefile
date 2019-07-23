NAME       := locust
IMAGE_NAME := renaudhager/locust

ifndef VERSION
  VERSION := $(shell git describe --abbrev=0 --tags --exact-match 2>/dev/null || git rev-parse --short HEAD)
endif

.PHONY: build
build:
	docker build \
	--tag="$(IMAGE_NAME):$(VERSION)" .

.PHONY: tag
tag:
	docker tag "$(IMAGE_NAME):$(VERSION)" \
	"$(IMAGE_NAME):latest"

.PHONY: push
push:
	docker push "$(IMAGE_NAME):latest"
