## ----------------------------------------------------------------------
## https://makefiletutorial.com/
## https://swcarpentry.github.io/make-novice/reference.html
## var ?= value - значение по умолчанию, $(var) - применение в команде
## ----------------------------------------------------------------------

.DEFAULT_GOAL := help
SHELL=/bin/bash
GH_WF_PATH=.github/workflows
ACT_RUN=act --bind --job
RED=\033[31m
NC=\033[0m

.PHONY: help
help:                       ## Show this help.
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

.PHONY: perm
perm:
	sudo chmod -R a+rw .

.PHONY: check_empty_files
check_empty_files:
	@$(ACT_RUN) check_empty_files

.PHONY: delete_empty_files
delete_empty_files:
	@$(ACT_RUN) delete_empty_files

.PHONY: init
init:
	@$(ACT_RUN) init

.PHONY: tests
tests:
	@$(ACT_RUN) tests

.PHONY: litter_up
litter_up:                  ## Загрязнение проекта
	@$(ACT_RUN) litter_up

.PHONY: ci
ci:                         ## Тестирование проекта
	@$(ACT_RUN) ci

backend_base_build:
	sudo docker build \
	-f docker/Dockerfile_backend_base \
	-t aibushin/t_api:backend_base \
	--build-arg poetry_version=1.8.3 \
	--no-cache \
	.

backend_base_ms_build:
	sudo docker build \
	-f docker/Dockerfile_backend_base_ms \
	-t aibushin/t_api:backend_base_ms \
	--build-arg poetry_version=1.8.3 \
	.

backend_dev:
	sudo docker build \
	--target dev \
	-f docker/Dockerfile_ms \
	-t aibushin/t_api:backend_dev \
	--build-arg poetry_version=1.8.3 \
	. \
	&& docker images |grep backend_dev \
	&& docker run -it --rm aibushin/t_api:backend_dev bash

backend_prod:
	sudo docker build \
	--target prod \
	-f docker/Dockerfile_ms \
	-t aibushin/t_api:backend_prod \
	--build-arg poetry_version=1.8.3 \
	. \
	&& docker images |grep backend_prod \
	&& docker run -it --rm aibushin/t_api:backend_prod bash

backend_base_push:
	docker push aibushin/t_api:backend_base

backend_base: backend_base_build backend_base_push

image_prune:
	docker image prune -af --filter "until=$(shell date +'%Y-%m-%dT%H:%M:%S' --date='-15 days')"
