# Hello World Codex Makefile

.PHONY: install test lint docs build clean validate setup pre-commit-install pre-commit-run

# Development setup
setup: install validate pre-commit-install
	@echo "✅ Development environment ready!"

install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

# Pre-commit hooks
pre-commit-install:
	@echo "🔧 Installing pre-commit hooks..."
	pip install pre-commit
	pre-commit install

pre-commit-run:
	@echo "🔍 Running pre-commit hooks..."
	pre-commit run --all-files

# Code quality
lint:
	@echo "🔍 Running code quality checks..."
	@echo "📝 Formatting Python files..."
	black scripts/ --exclude="refactor_codex_structure.py"
	@echo "📝 Sorting imports..."
	isort scripts/ --skip="refactor_codex_structure.py"
	@echo "🔍 Running flake8..."
	flake8 scripts/ --exclude="refactor_codex_structure.py" --max-line-length=88 --extend-ignore=E203,W503

# Testing
test:
	@echo "🧪 Running tests..."
	pytest --cov=. --cov-report=html

# Documentation
docs:
	@echo "📚 Starting documentation server..."
	mkdocs serve

build-docs:
	@echo "📖 Building documentation..."
	mkdocs build

# Docker
build:
	@echo "🐳 Building Docker image..."
	docker build -t hello-world-codex .

run:
	@echo "🚀 Running Docker container..."
	docker run -p 8000:8000 hello-world-codex

# Environment validation
validate:
	@echo "🔧 Validating environment..."
	python scripts/validate_env.py

# Code generation
generate-plan:
	@echo "🧠 Generating codex plan..."
	python scripts/generate_codex_plan.py

# Codex validation and refactoring
validate-codex:
	@echo "🔍 Validating codex structure..."
	python scripts/validate_codex_structure.py

refactor-codex:
	@echo "🔄 Refactoring codex structure..."
	python scripts/simple_refactor_codex.py

# Cleanup
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov/
	rm -rf site/

# Requirements management
compile-requirements:
	@echo "📦 Compiling requirements..."
	pip-compile requirements.in --output-file=requirements.txt

# Help
help:
	@echo "Hello World Codex - Available commands:"
	@echo "  setup              - Complete development setup"
	@echo "  install            - Install dependencies"
	@echo "  pre-commit-install - Install pre-commit hooks"
	@echo "  pre-commit-run     - Run pre-commit hooks"
	@echo "  lint               - Run code quality checks"
	@echo "  test               - Run tests with coverage"
	@echo "  docs               - Start documentation server"
	@echo "  build-docs         - Build documentation"
	@echo "  build              - Build Docker image"
	@echo "  run                - Run Docker container"
	@echo "  validate           - Validate environment"
	@echo "  generate-plan      - Generate implementation plan"
	@echo "  validate-codex     - Validate codex structure"
	@echo "  refactor-codex     - Refactor codex structure"
	@echo "  clean              - Clean up generated files"
	@echo "  compile-requirements - Compile requirements.txt"
	@echo "  help               - Show this help message"
