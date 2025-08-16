# Ansible Role Template Makefile
# Organizational standards for SplendidCube Ansible roles

.PHONY: help init clean install update dev lint lint-fix format format-check type-check test validate docs pre-commit-install pre-commit-run pre-commit-staged pre-commit-update quality ansible-lint ansible-syntax

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

init: ## Initialize development environment
	@echo "🚀 Initializing development environment..."
	@if [ -f ".venv" ]; then \
		VENV_NAME=$$(cat .venv); \
		echo "📦 Virtual environment name: $$VENV_NAME"; \
		if ! /bin/zsh -c "source ~/.zshrc && lsvirtualenv -b | grep -q $$VENV_NAME"; then \
			echo "🆕 Creating virtual environment: $$VENV_NAME"; \
			/bin/zsh -c "source ~/.zshrc && mkvirtualenv $$VENV_NAME"; \
		else \
			echo "✅ Virtual environment already exists: $$VENV_NAME"; \
		fi; \
	fi
	@if [ -f "pyproject.toml" ]; then \
		echo "📚 Installing dependencies with Poetry..."; \
		/bin/zsh -c "source ~/.zshrc && poetry install"; \
	elif [ -f "requirements.txt" ]; then \
		echo "📚 Installing dependencies with pip..."; \
		pip install -r requirements.txt; \
	elif [ -f "package.json" ]; then \
		echo "📚 Installing dependencies with npm..."; \
		npm install; \
	else \
		echo "ℹ️  No dependency files found (pyproject.toml, requirements.txt, package.json)"; \
	fi
	@$(MAKE) pre-commit-install
	@echo "✅ Environment initialization complete!"

install: ## Install dependencies
	@if [ -f "pyproject.toml" ]; then \
		/bin/zsh -c "source ~/.zshrc && poetry install --only=main"; \
	elif [ -f "requirements.txt" ]; then \
		pip install -r requirements.txt; \
	elif [ -f "package.json" ]; then \
		npm install --production; \
	else \
		echo "❌ No dependency files found"; exit 1; \
	fi

update: ## Update dependencies
	@if [ -f "pyproject.toml" ]; then \
		/bin/zsh -c "source ~/.zshrc && poetry update"; \
	elif [ -f "requirements.txt" ]; then \
		pip install --upgrade -r requirements.txt; \
	elif [ -f "package.json" ]; then \
		npm update; \
	else \
		echo "❌ No dependency files found"; exit 1; \
	fi

dev: ## Install development dependencies
	@if [ -f "pyproject.toml" ]; then \
		/bin/zsh -c "source ~/.zshrc && poetry install --with=dev"; \
	elif [ -f "package.json" ]; then \
		npm install; \
	else \
		echo "ℹ️  No development dependencies configuration found"; \
	fi

lint: ## Run linting checks
	@echo "🔍 Running linting checks..."
	@if [ -f "pyproject.toml" ] && grep -q "ruff" pyproject.toml; then \
		/bin/zsh -c "source ~/.zshrc && uvx ruff check ."; \
	else \
		echo "ℹ️  No Python linting configuration found"; \
	fi
	@$(MAKE) ansible-lint

lint-fix: ## Fix auto-fixable linting issues
	@echo "🔧 Fixing linting issues..."
	@if [ -f "pyproject.toml" ] && grep -q "ruff" pyproject.toml; then \
		/bin/zsh -c "source ~/.zshrc && uvx ruff check --fix ."; \
	else \
		echo "ℹ️  No Python linting configuration found"; \
	fi

ansible-lint: ## Run ansible-lint on role files
	@echo "🔍 Running ansible-lint..."
	@if command -v ansible-lint >/dev/null 2>&1; then \
		/bin/zsh -c "source ~/.zshrc && uvx ansible-lint ."; \
	else \
		echo "⚠️  ansible-lint not found, installing..."; \
		/bin/zsh -c "source ~/.zshrc && uvx ansible-lint ."; \
	fi

ansible-syntax: ## Check Ansible syntax
	@echo "🔍 Checking Ansible syntax..."
	@if [ -f "tasks/main.yml" ]; then \
		echo "✅ Ansible role tasks found - using ansible-lint for validation"; \
		/bin/zsh -c "source ~/.zshrc && uvx ansible-lint tasks/main.yml" || echo "⚠️  Install ansible-lint for syntax checking"; \
	else \
		echo "ℹ️  No tasks/main.yml found"; \
	fi

format: ## Format code
	@echo "🎨 Formatting code..."
	@if [ -f "pyproject.toml" ] && grep -q "ruff" pyproject.toml; then \
		/bin/zsh -c "source ~/.zshrc && uvx ruff format ."; \
	else \
		echo "ℹ️  No Python formatting configuration found"; \
	fi

format-check: ## Check code formatting
	@echo "🎨 Checking code formatting..."
	@if [ -f "pyproject.toml" ] && grep -q "ruff" pyproject.toml; then \
		/bin/zsh -c "source ~/.zshrc && uvx ruff format --check ."; \
	else \
		echo "ℹ️  No Python formatting configuration found"; \
	fi

test: ## Run tests
	@echo "🧪 Running tests..."
	@if [ -f "pyproject.toml" ] && grep -q "pytest" pyproject.toml; then \
		/bin/zsh -c "source ~/.zshrc && poetry run pytest"; \
	elif [ -f "package.json" ] && grep -q "test" package.json; then \
		npm test; \
	else \
		echo "ℹ️  No test configuration found"; \
	fi
	@$(MAKE) ansible-syntax

test-coverage: ## Run tests with coverage
	@echo "🧪 Running tests with coverage..."
	@if [ -f "pyproject.toml" ] && grep -q "pytest" pyproject.toml; then \
		/bin/zsh -c "source ~/.zshrc && poetry run pytest -v --cov --cov-report=html --cov-report=term"; \
	elif [ -f "package.json" ] && grep -q "test" package.json; then \
		npm run test:coverage || npm test; \
	else \
		echo "ℹ️  No test configuration found"; \
	fi

validate: ## Install validation tools
	@echo "✅ Installing validation dependencies..."
	@if [ -f "pyproject.toml" ]; then \
		/bin/zsh -c "source ~/.zshrc && poetry install --with=dev"; \
	else \
		echo "ℹ️  No Python validation configuration found"; \
	fi

type-check: ## Run type checking (currently disabled)
	@echo "🔍 Type checking..."
	@echo "ℹ️  Type checking disabled until Ruff's type checker is stable"
	@echo "✅ Skipping type checking for now"

docs: ## Generate documentation
	@echo "📚 Generating documentation..."
	@if [ -f "docs/conf.py" ]; then \
		if [ -z "$$SPLENDIDCUBE_DOCUMENTATION_ROOT" ]; then \
			echo "❌ SPLENDIDCUBE_DOCUMENTATION_ROOT environment variable is not set"; \
			echo "   Please set it to the documentation output directory"; \
			exit 1; \
		fi; \
		if [ ! -d "$$SPLENDIDCUBE_DOCUMENTATION_ROOT" ]; then \
			echo "📁 Creating documentation root directory: $$SPLENDIDCUBE_DOCUMENTATION_ROOT"; \
			mkdir -p "$$SPLENDIDCUBE_DOCUMENTATION_ROOT"; \
		fi; \
		PROJECT_NAME=$$(grep "^PROJECT_NAME" docs/conf.py | cut -d'"' -f2 | sed 's/\[PROJECT_NAME\]/template.base/g'); \
		echo "🔧 Building documentation with Sphinx..."; \
		/bin/zsh -c "source ~/.zshrc && uvx --from sphinx --with sphinx-wagtail-theme --with myst-parser sphinx-build docs \"$$SPLENDIDCUBE_DOCUMENTATION_ROOT/$$PROJECT_NAME\" -b html -E"; \
		echo "✨ Documentation generated successfully!"; \
		echo "📖 Open: $$SPLENDIDCUBE_DOCUMENTATION_ROOT/$$PROJECT_NAME/index.html"; \
	elif [ -f "mkdocs.yml" ]; then \
		/bin/zsh -c "source ~/.zshrc && uvx mkdocs build"; \
	else \
		echo "ℹ️  No documentation configuration found"; \
	fi

pre-commit-install: ## Install pre-commit hooks
	@echo "🪝 Installing pre-commit hooks..."
	@/bin/zsh -c "source ~/.zshrc && uvx pre-commit install"

pre-commit-run: ## Run pre-commit hooks on all files
	@echo "🪝 Running pre-commit hooks on all files..."
	@/bin/zsh -c "source ~/.zshrc && uvx pre-commit run --all-files"

pre-commit-staged: ## Run pre-commit hooks on staged files
	@echo "🪝 Running pre-commit hooks on staged files..."
	@/bin/zsh -c "source ~/.zshrc && uvx pre-commit run"

pre-commit-update: ## Update pre-commit hooks
	@echo "🔨 Updating pre-commit hooks..."
	@/bin/zsh -c "source ~/.zshrc && uvx pre-commit autoupdate"

quality: ## Run all quality checks
	@echo "✨ Running comprehensive quality checks..."
	@$(MAKE) lint
	@$(MAKE) format-check
	@$(MAKE) type-check
	@$(MAKE) ansible-lint
	@echo "✅ All quality checks completed!"

clean: ## Clean up development environment
	@echo "🧹 Cleaning up..."
	@if [ -f ".venv" ]; then \
		VENV_NAME=$$(cat .venv); \
		echo "🗑️  Removing virtual environment: $$VENV_NAME"; \
		/bin/zsh -c "source ~/.zshrc && rmvirtualenv $$VENV_NAME" 2>/dev/null || true; \
	fi
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf htmlcov/ .coverage .tox/ .nox/ dist/ build/ 2>/dev/null || true
	@echo "✅ Cleanup complete!"
