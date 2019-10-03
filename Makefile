# VARIABLES ARGUMENTS
message=auto generate
settings=challenge.settings.development
deploy_message=$(shell git log --oneline -1)
limit=30
page=1

ifdef SIMPLE_SETTINGS
	settings=$(SIMPLE_SETTINGS)
else
	export SIMPLE_SETTINGS=$(settings)
endif

export PYTHONPATH=$(shell pwd)/src/
export PYTHONDONTWRITEBYTECODE=1
export DJANGO_SETTINGS_MODULE=$(settings)

.PHONY: help

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

clean: ## Clean local environment
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -rf htmlcov/
	@rm -f coverage.xml
	@rm -f *.log

doc: ## Start server of MkDocs
	mkdocs serve

doc-build: ## Build the documentation
	mkdocs build --clean

outdated: ## Show outdated dependencies
	@pip list --outdated --format=columns

dependencies: ## Install development dependencies
	pip install -U -r requirements/dev.txt

run: ## Run application server
	gunicorn challenge:app --worker-class aiohttp.GunicornUVLoopWebWorker --reload

test: clean ## Run tests
	pytest -x

test-matching: clean ## Run matching tests
	pytest -x -k $(q) --pdb

test-debug: clean ## Run tests with pdb
	pytest -x --pdb

test-coverage: clean ## Run tests with coverage
	pytest -x --cov=src/challenge/ --cov-report=term-missing --cov-report=xml

test-coverage-html: clean ## Run tests with coverage with html report
	pytest -x --cov=src/challenge/ --cov-report=html:htmlcov

lint: ## Run code lint
	flake8 --show-source .
	isort --check

fix-python-import: ## Organize python imports
	isort -rc .

empty-migration: ## Generate empty migrations
	@django-admin makemigrations --empty $(app)

migrate: ## Apply migrations
	@django-admin migrate

migration: ## Generate migrations
	@django-admin makemigrations

detect-migrations:  ## Detect missing migrations
	@django-admin makemigrations --dry-run --noinput | grep 'No changes detected' -q || (echo 'Missing migration detected!' && exit 1)

shell: ## Run repl
	@echo 'Loading shell with settings = $(settings)'
	@PYTHONSTARTUP=.startup.py ipython

safety-check: ## Checks libraries safety
	safety check -r requirements/prod.txt
	safety check -r requirements/base.txt
	safety check -r requirements/test.txt
	safety check -r requirements/dev.txt

create-app: ## Create new App for Challenge
	@django-admin create_app $(name)

list-apps: ## List Apps from Challenge
	@django-admin list_apps --app=$(app) --is-active=$(isactive) --limit=$(limit) --page=$(page)
