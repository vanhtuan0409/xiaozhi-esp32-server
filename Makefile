REPO:=ghcr.io/vanhtuan0409/xiaozhi-server
TAG:=$(shell date +%Y%m%d)-$(shell date +%s)

build-server:
	docker build -t $(REPO):$(TAG) -f Dockerfile-server .
