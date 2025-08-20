# Makefile for WB_Anki maintenance tasks

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
UV := uv

# Help target
help: ## Display this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@echo "  install-deps     Install production dependencies"
	@echo "  install-dev-deps Install development dependencies"
	@echo "  install-all      Install all dependencies (prod + dev)"
	@echo "  test             Run tests"
	@echo "  test-cov         Run tests with coverage"
	@echo "  pre-commit       Run all pre-commit hooks"
	@echo "  format           Format code with black and isort"
	@echo "  lint             Run linting checks"
	@echo "  type-check       Run type checking"
	@echo "  check            Run all code quality checks"
	@echo "  clean            Clean up temporary files"
	@echo "  help             Display this help message"

# Dependency installation targets
install-deps: ## Install production dependencies
	$(UV) sync --frozen

install-dev-deps: ## Install development dependencies
	$(UV) sync --frozen --extra dev

install-all: ## Install all dependencies (prod + dev)
	$(UV) sync --frozen --all-extras

# Test targets
test: ## Run tests
	$(UV) run pytest

test-cov: ## Run tests with coverage
	$(UV) run pytest --cov=src --cov-report=term-missing

# Pre-commit targets
pre-commit: ## Run all pre-commit hooks
	$(UV) run pre-commit run --all-files

# Code quality targets
format: ## Format code with black and isort
	$(UV) run black src/ tests/
	$(UV) run isort src/ tests/

lint: ## Run linting checks
	$(UV) run flake8 src/ tests/

type-check: ## Run type checking
	$(UV) run mypy src/

check: ## Run all code quality checks
	@echo "Running code formatting..."
	$(UV) run black --check src/ tests/
	@echo "Running import sorting check..."
	$(UV) run isort --check-only src/ tests/
	@echo "Running linting checks..."
	$(UV) run flake8 src/ tests/
	@echo "Running type checking..."
	$(UV) run mypy src/
	@echo "All code quality checks passed!"

# Clean target
clean: ## Clean up temporary files
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyc" -delete

# Phony targets
.PHONY: help install-deps install-dev-deps install-all test test-cov pre-commit format lint type-check check clean