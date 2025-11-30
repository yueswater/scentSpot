# Makefile for Django ScentSpot Project
# Requires: Poetry, Python 3.8+

# Variables
POETRY := poetry
PYTHON := $(POETRY) run python
MANAGE := $(PYTHON) manage.py
APP_NAME := logapp

# Colors for output
COLOR_RESET := \033[0m
COLOR_GREEN := \033[32m
COLOR_YELLOW := \033[33m
COLOR_BLUE := \033[34m

# Default target
.DEFAULT_GOAL := help

##@ General

.PHONY: help
help: ## Display this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Setup

.PHONY: install
install: ## Install all dependencies via Poetry
	@echo "$(COLOR_BLUE)Installing dependencies...$(COLOR_RESET)"
	$(POETRY) install

.PHONY: install-dev
install-dev: ## Install dependencies including dev packages
	@echo "$(COLOR_BLUE)Installing dev dependencies...$(COLOR_RESET)"
	$(POETRY) install --with dev

.PHONY: update
update: ## Update all dependencies
	@echo "$(COLOR_BLUE)Updating dependencies...$(COLOR_RESET)"
	$(POETRY) update

##@ Database

.PHONY: migrate
migrate: ## Run database migrations
	@echo "$(COLOR_BLUE)Running migrations...$(COLOR_RESET)"
	$(MANAGE) migrate

.PHONY: makemigrations
makemigrations: ## Create new migrations based on model changes
	@echo "$(COLOR_BLUE)Creating migrations...$(COLOR_RESET)"
	$(MANAGE) makemigrations

.PHONY: showmigrations
showmigrations: ## Show all migrations and their status
	@echo "$(COLOR_BLUE)Showing migrations...$(COLOR_RESET)"
	$(MANAGE) showmigrations

.PHONY: db-reset
db-reset: ## Reset database (WARNING: destroys all data)
	@echo "$(COLOR_YELLOW)WARNING: This will delete all data!$(COLOR_RESET)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(MANAGE) flush --no-input; \
		echo "$(COLOR_GREEN)Database reset complete$(COLOR_RESET)"; \
	fi

##@ Static Files

.PHONY: collectstatic
collectstatic: ## Collect static files
	@echo "$(COLOR_BLUE)Collecting static files...$(COLOR_RESET)"
	$(MANAGE) collectstatic --no-input --clear

.PHONY: findstatic
findstatic: ## Find a static file (usage: make findstatic FILE=images/fluffy.png)
	@echo "$(COLOR_BLUE)Finding static file: $(FILE)$(COLOR_RESET)"
	$(MANAGE) findstatic $(FILE)

##@ Development Server

.PHONY: run
run: collectstatic ## Collect static files and run development server
	@echo "$(COLOR_GREEN)Starting development server...$(COLOR_RESET)"
	$(MANAGE) runserver

.PHONY: runserver
runserver: run ## Alias for 'run' target

.PHONY: run-plus
run-plus: collectstatic migrate ## Collect static, migrate, then run server
	@echo "$(COLOR_GREEN)Starting development server...$(COLOR_RESET)"
	$(MANAGE) runserver

.PHONY: run-custom
run-custom: collectstatic ## Run server on custom host:port (usage: make run-custom HOST=0.0.0.0 PORT=8080)
	@echo "$(COLOR_GREEN)Starting development server on $(HOST):$(PORT)...$(COLOR_RESET)"
	$(MANAGE) runserver $(HOST):$(PORT)

##@ User Management

.PHONY: createsuperuser
createsuperuser: ## Create a superuser account
	@echo "$(COLOR_BLUE)Creating superuser...$(COLOR_RESET)"
	$(MANAGE) createsuperuser

.PHONY: changepassword
changepassword: ## Change user password (usage: make changepassword USER=username)
	@echo "$(COLOR_BLUE)Changing password for $(USER)...$(COLOR_RESET)"
	$(MANAGE) changepassword $(USER)

##@ Testing

.PHONY: test
test: ## Run all tests
	@echo "$(COLOR_BLUE)Running tests...$(COLOR_RESET)"
	$(MANAGE) test

.PHONY: test-app
test-app: ## Run tests for specific app (usage: make test-app APP=logapp)
	@echo "$(COLOR_BLUE)Running tests for $(APP)...$(COLOR_RESET)"
	$(MANAGE) test $(APP)

.PHONY: coverage
coverage: ## Run tests with coverage report
	@echo "$(COLOR_BLUE)Running tests with coverage...$(COLOR_RESET)"
	$(POETRY) run coverage run --source='.' manage.py test
	$(POETRY) run coverage report
	$(POETRY) run coverage html
	@echo "$(COLOR_GREEN)Coverage report generated in htmlcov/index.html$(COLOR_RESET)"

##@ Code Quality

.PHONY: lint
lint: ## Run linting checks
	@echo "$(COLOR_BLUE)Running linting...$(COLOR_RESET)"
	$(POETRY) run flake8 $(APP_NAME)

.PHONY: format
format: ## Format code with black
	@echo "$(COLOR_BLUE)Formatting code...$(COLOR_RESET)"
	$(POETRY) run black $(APP_NAME)

.PHONY: format-check
format-check: ## Check code formatting without changes
	@echo "$(COLOR_BLUE)Checking code format...$(COLOR_RESET)"
	$(POETRY) run black --check $(APP_NAME)

.PHONY: isort
isort: ## Sort imports
	@echo "$(COLOR_BLUE)Sorting imports...$(COLOR_RESET)"
	$(POETRY) run isort $(APP_NAME)

.PHONY: check
check: format-check lint ## Run all code quality checks

##@ Django Shell

.PHONY: shell
shell: ## Open Django shell
	@echo "$(COLOR_BLUE)Opening Django shell...$(COLOR_RESET)"
	$(MANAGE) shell

.PHONY: shell-plus
shell-plus: ## Open enhanced Django shell (requires django-extensions)
	@echo "$(COLOR_BLUE)Opening Django shell plus...$(COLOR_RESET)"
	$(MANAGE) shell_plus

.PHONY: dbshell
dbshell: ## Open database shell
	@echo "$(COLOR_BLUE)Opening database shell...$(COLOR_RESET)"
	$(MANAGE) dbshell

##@ Utilities

.PHONY: clean
clean: ## Clean up temporary files and cache
	@echo "$(COLOR_BLUE)Cleaning up...$(COLOR_RESET)"
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '.coverage' -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf staticfiles/
	@echo "$(COLOR_GREEN)Cleanup complete$(COLOR_RESET)"

.PHONY: logs
logs: ## Show Django development server logs (requires server to be running)
	@echo "$(COLOR_BLUE)Showing logs...$(COLOR_RESET)"
	tail -f logs/django.log

.PHONY: check-deps
check-deps: ## Check for outdated dependencies
	@echo "$(COLOR_BLUE)Checking for outdated dependencies...$(COLOR_RESET)"
	$(POETRY) show --outdated

.PHONY: show-urls
show-urls: ## Show all URL patterns
	@echo "$(COLOR_BLUE)Showing URL patterns...$(COLOR_RESET)"
	$(MANAGE) show_urls

##@ Fixtures

.PHONY: dumpdata
dumpdata: ## Dump data to JSON file (usage: make dumpdata APP=logapp MODEL=Perfume)
	@echo "$(COLOR_BLUE)Dumping data...$(COLOR_RESET)"
	$(MANAGE) dumpdata $(APP).$(MODEL) --indent 2 > fixtures/$(APP)_$(MODEL).json
	@echo "$(COLOR_GREEN)Data dumped to fixtures/$(APP)_$(MODEL).json$(COLOR_RESET)"

.PHONY: loaddata
loaddata: ## Load data from fixture file (usage: make loaddata FILE=fixtures/data.json)
	@echo "$(COLOR_BLUE)Loading fixture: $(FILE)$(COLOR_RESET)"
	$(MANAGE) loaddata $(FILE)

##@ Production

.PHONY: prod-check
prod-check: ## Run Django deployment checks
	@echo "$(COLOR_BLUE)Running deployment checks...$(COLOR_RESET)"
	$(MANAGE) check --deploy

.PHONY: prod-static
prod-static: ## Collect static files for production
	@echo "$(COLOR_BLUE)Collecting static files for production...$(COLOR_RESET)"
	$(MANAGE) collectstatic --no-input --clear
	@echo "$(COLOR_GREEN)Static files collected$(COLOR_RESET)"

.PHONY: prod-migrate
prod-migrate: ## Run migrations for production
	@echo "$(COLOR_BLUE)Running production migrations...$(COLOR_RESET)"
	$(MANAGE) migrate --no-input

##@ Docker (if using Docker)

.PHONY: docker-build
docker-build: ## Build Docker image
	@echo "$(COLOR_BLUE)Building Docker image...$(COLOR_RESET)"
	docker-compose build

.PHONY: docker-up
docker-up: ## Start Docker containers
	@echo "$(COLOR_BLUE)Starting Docker containers...$(COLOR_RESET)"
	docker-compose up -d

.PHONY: docker-down
docker-down: ## Stop Docker containers
	@echo "$(COLOR_BLUE)Stopping Docker containers...$(COLOR_RESET)"
	docker-compose down

.PHONY: docker-logs
docker-logs: ## Show Docker container logs
	@echo "$(COLOR_BLUE)Showing Docker logs...$(COLOR_RESET)"
	docker-compose logs -f

##@ Quick Commands

.PHONY: dev
dev: install migrate collectstatic ## Full development setup (install, migrate, collectstatic)
	@echo "$(COLOR_GREEN)Development environment ready!$(COLOR_RESET)"
	@echo "$(COLOR_YELLOW)Run 'make run' to start the server$(COLOR_RESET)"

.PHONY: fresh
fresh: clean install migrate collectstatic ## Fresh install (clean, install, migrate, collectstatic)
	@echo "$(COLOR_GREEN)Fresh installation complete!$(COLOR_RESET)"
	@echo "$(COLOR_YELLOW)Run 'make run' to start the server$(COLOR_RESET)"

.PHONY: quick
quick: collectstatic ## Quick start (just collectstatic and run)
	@echo "$(COLOR_GREEN)Quick starting server...$(COLOR_RESET)"
	$(MANAGE) runserver

##@ Information

.PHONY: info
info: ## Show project information
	@echo "$(COLOR_BLUE)Project Information:$(COLOR_RESET)"
	@echo "  Poetry version: $$($(POETRY) --version)"
	@echo "  Python version: $$($(PYTHON) --version)"
	@echo "  Django version: $$($(MANAGE) version)"
	@echo "  App name: $(APP_NAME)"

.PHONY: settings
settings: ## Show current Django settings
	@echo "$(COLOR_BLUE)Django Settings:$(COLOR_RESET)"
	$(MANAGE) diffsettings

# Prevent make from treating file names as targets
.PHONY: all