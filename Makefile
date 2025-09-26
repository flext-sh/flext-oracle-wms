# FLEXT-ORACLE-WMS Makefile
PROJECT_NAME := flext-oracle-wms
PYTHON_VERSION := 3.13
POETRY := poetry
SRC_DIR := src
TESTS_DIR := tests

# Quality standards
MIN_COVERAGE := 100

# WMS configuration
ORACLE_WMS_HOST := localhost
ORACLE_WMS_PORT := 1521
WMS_ENVIRONMENT := development

# Help
help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

# Installation
install: ## Install dependencies
	$(POETRY) install

install-dev: ## Install dev dependencies
	$(POETRY) install --with dev,test,docs

setup: install-dev ## Complete project setup
	$(POETRY) run pre-commit install

# Quality gates
validate: lint type-check security test ## Run all quality gates (MANDATORY ORDER)

check: lint type-check ## Quick health check

lint: ## Run linting (ZERO TOLERANCE)
	$(POETRY) run ruff check .

format: ## Format code
	$(POETRY) run ruff format .

type-check: ## Run type checking with Pyrefly (ZERO TOLERANCE)
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pyrefly check .

security: ## Run security scanning
	$(POETRY) run bandit -r $(SRC_DIR)
	$(POETRY) run pip-audit

fix: ## Auto-fix issues
	$(POETRY) run ruff check . --fix
	$(POETRY) run ruff format .

# Testing
test: ## Run tests with 100% coverage (MANDATORY)
	$(POETRY) run pytest $(TESTS_DIR) --cov=$(SRC_DIR) --cov-report=term-missing --cov-fail-under=$(MIN_COVERAGE)

test-unit: ## Run unit tests
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -m "not integration" -v

test-integration: ## Run integration tests with Docker
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -m integration -v

test-wms: ## Run WMS specific tests
	$(POETRY) run pytest $(TESTS_DIR) -m wms -v

test-oracle: ## Run Oracle database tests
	$(POETRY) run pytest $(TESTS_DIR) -m oracle -v

test-inventory: ## Run inventory tests
	$(POETRY) run pytest $(TESTS_DIR) -m inventory -v

test-shipping: ## Run shipping tests
	$(POETRY) run pytest $(TESTS_DIR) -m shipping -v

test-fast: ## Run tests without coverage
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -v

coverage-html: ## Generate HTML coverage report
	$(POETRY) run pytest $(TESTS_DIR) --cov=$(SRC_DIR) --cov-report=html

# WMS operations
wms-test: ## Test WMS connectivity
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c "from flext_oracle_wms import test_wms_connectivity; test_wms_connectivity()"

wms-schema: ## Validate WMS schema
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c "from flext_oracle_wms import validate_wms_schema; validate_wms_schema()"

wms-inventory: ## Test inventory operations
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c "from flext_oracle_wms import test_inventory_operations; test_inventory_operations()"

wms-shipping: ## Test shipping operations
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c "from flext_oracle_wms import test_shipping_operations; test_shipping_operations()"

# Oracle operations
oracle-connect: ## Test Oracle connection
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c "from flext_oracle_wms import test_oracle_connection; test_oracle_connection()"

oracle-schema: ## Validate Oracle schema
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c "from flext_oracle_wms import validate_oracle_schema; validate_oracle_schema()"

# Build
build: ## Build package
	$(POETRY) build

build-clean: clean build ## Clean and build

# Documentation
docs: ## Build documentation
	$(POETRY) run mkdocs build

docs-serve: ## Serve documentation
	$(POETRY) run mkdocs serve

# Dependencies
deps-update: ## Update dependencies
	$(POETRY) update

deps-show: ## Show dependency tree
	$(POETRY) show --tree

deps-audit: ## Audit dependencies
	$(POETRY) run pip-audit

# Development
shell: ## Open Python shell
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python

pre-commit: ## Run pre-commit hooks
	$(POETRY) run pre-commit run --all-files

# Maintenance
clean: ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ htmlcov/ .coverage .mypy_cache/ .pyrefly_cache/ .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

clean-all: clean ## Deep clean including venv
	rm -rf .venv/

reset: clean-all setup ## Reset project

# Diagnostics
diagnose: ## Project diagnostics
	@echo "Python: $$(python --version)"
	@echo "Poetry: $$($(POETRY) --version)"
	@echo "Oracle WMS: $$(PYTHONPATH=$(SRC_DIR) $(POETRY) run python -c 'import flext_oracle_wms; print(flext_oracle_wms.__version__)' 2>/dev/null || echo 'Not available')"
	@$(POETRY) env info

doctor: diagnose check ## Health check

# Docker Operations - MAXIMUM CONTAINER USAGE AS REQUESTED
docker-build: ## Build Docker images
	docker-compose build --no-cache

docker-up: ## Start all Docker services
	docker-compose up -d

docker-down: ## Stop all Docker services
	docker-compose down --volumes --remove-orphans

docker-examples: ## Run Oracle WMS examples in Docker (COMPLETE FUNCTIONALITY)
	./docker-run.sh examples

docker-test: ## Run complete test suite in Docker with real Oracle WMS
	./docker-run.sh test

docker-validate: ## Complete Oracle WMS validation using Docker (USER REQUESTED)
	./docker-run.sh all

docker-logs: ## Show Docker container logs
	docker-compose logs -f

docker-clean: ## Clean Docker resources
	./docker-run.sh clean

docker-shell: ## Access Docker container shell
	docker-compose run --rm flext-oracle-wms /bin/bash

docker-coverage: ## Generate coverage report using Docker
	docker-compose run --rm flext-oracle-wms-test

# Complete Docker workflow (USER'S MAIN REQUEST)
docker-full-validation: docker-build docker-validate ## Complete Docker validation workflow
	@echo "🎉 COMPLETE DOCKER VALIDATION FINISHED!"
	@echo "📊 Check ./reports/ for detailed results"

# Aliases
t: test
l: lint
f: format
tc: type-check
c: clean
i: install
v: validate
dv: docker-validate
dt: docker-test
de: docker-examples

.DEFAULT_GOAL := help
.PHONY: help install install-dev setup validate check lint format type-check security fix test test-unit test-integration test-wms test-oracle test-inventory test-shipping test-fast coverage-html wms-test wms-schema wms-inventory wms-shipping oracle-connect oracle-schema build build-clean docs docs-serve deps-update deps-show deps-audit shell pre-commit clean clean-all reset diagnose doctor docker-build docker-up docker-down docker-examples docker-test docker-validate docker-logs docker-clean docker-shell docker-coverage docker-full-validation t l f tc c i v dv dt de