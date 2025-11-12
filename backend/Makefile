## ----------------------------------------------------------------------
## https://makefiletutorial.com/
## https://swcarpentry.github.io/make-novice/reference.html
## var ?= value - значение по умолчанию, $(var) - применение в команде
## ----------------------------------------------------------------------

.DEFAULT_GOAL := help
SHELL=/bin/bash
POETRY_RUN = poetry --quiet run
RED=\033[31m
NC=\033[0m

.PHONY: run help

.PHONY: help
help:                       ## Show this help.
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

.PHONY: lint
lint:                       ## Линтинг кода.
	@$(POETRY_RUN) ruff check .

.PHONY: format
format:                     ## Форматирование кода.
	@$(POETRY_RUN) ruff check --fix .
	@$(POETRY_RUN) toml-sort --in-place pyproject.toml

.PHONY: db_mm
db_mm:                      ## Создать файл миграции БД.
ifdef name
	@$(POETRY_RUN) alembic revision --autogenerate -m "$(name)"
else
	@echo -e "$(RED)Параметр name - обязателен!$(NC) - make $@ name=\"some text\""
	@exit 1
endif

.PHONY: db_migrate
db_migrate:                 ## Миграция БД.
	@$(POETRY_RUN) alembic upgrade head

.PHONY: db_check
db_check: db_migrate        ## Проверка необходимости создания миграции.
	@$(POETRY_RUN) alembic check

# .PHONY: run
# run: db_migrate             ## Запуск сервиса.
.PHONY: run
run:
	python -m src.main

.PHONY: test
test: db_check lint         ## Тестирование кода.

.PHONY: wait
wait:
	tail -f /dev/null

.PHONY: bump-version
bump-version:
	poetry version $(v)
	$(POETRY_RUN) python -m scripts.update_issue_templates $(v)
	git add . && git commit -m "chore(release): bump version to $(v)"
	git tag -a $(v) -m ""
