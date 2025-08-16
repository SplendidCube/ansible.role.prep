# Project Structure

This document outlines the directory structure and key files in the `[PROJECT_NAME]` project.

## Root Directory Structure

```text
[PROJECT_NAME]/
├── README.md                        # Project overview and usage
├── makefile                         # Build and development targets
├── .editorconfig                    # Editor consistency settings
├── .gitignore                       # Git ignore patterns
├── .pre-commit-config.yaml          # Quality automation hooks
├── [Technology-specific files]      # pyproject.toml, Cargo.toml, package.json, etc.
├── docs/                            # Sphinx documentation
│   ├── conf.py
│   ├── index.md
│   ├── project-structure.md
│   ├── deployment.md
│   ├── _static/
│   └── _templates/
├── src/ or lib/                     # Source code (structure varies by technology)
└── tests/                           # Test files
```

## Key Files and Directories

- **README.md**: Project overview, usage, and comprehensive documentation
- **makefile**: Build, test, lint, and documentation targets for all supported technologies
- **.editorconfig**: Consistent editor settings across IDEs and team members
- **.gitignore**: Comprehensive ignore patterns for all supported technologies
- **.pre-commit-config.yaml**: Quality automation with conventional commits validation
- **Technology files**: Dependencies and configuration (pyproject.toml, Cargo.toml, package.json)
- **docs/**: Sphinx documentation sources with MyST Markdown support

## Supported Technologies

### Python Projects

- **Poetry**: Dependency management (pyproject.toml)
- **Ruff**: Linting and formatting
- **pytest**: Unit testing
- **MyPy**: Type checking (optional)
- **Sphinx**: Documentation generation

### Rust Projects

- **Cargo**: Build system and package manager
- **clippy**: Linting
- **rustfmt**: Code formatting
- **cargo test**: Testing

### JavaScript/TypeScript Projects

- **npm/yarn**: Package management
- **ESLint**: Linting
- **Prettier**: Code formatting
- **Jest/Vitest**: Testing

### Ansible Projects

- **ansible-lint**: Role and playbook validation
- **molecule**: Testing framework (when applicable)

### Docker Projects

- **hadolint**: Dockerfile linting
- **docker-compose**: Multi-container orchestration

## Development and Quality Tools

All projects include:

- **Pre-commit hooks**: Automated quality checks and formatting
- **Conventional commits**: Enforced commit message format validation
- **Security scanning**: Bandit for Python, other security tools as applicable
- **Documentation**: Consistent Sphinx documentation with MyST Markdown
- **CI/CD**: GitHub Actions validation workflow

## Build System

Use the `makefile` for technology-agnostic targets:

- Environment initialization (`make init`)
- Code quality checks (`make quality`)
- Linting (`make lint`, `make lint-fix`)
- Formatting (`make format`, `make format-check`)
- Testing (`make test`)
- Documentation generation (`make docs`)
- Pre-commit management (`make pre-commit-install`, `make pre-commit-run`)
- Environment cleanup (`make clean`)

## Environment Management

- **Python**: Poetry with uvx for tool execution
- **Rust**: Cargo manages everything
- **JavaScript/TypeScript**: npm/yarn for dependencies
- **Editor consistency**: EditorConfig for all file types

## Quality Assurance

All projects enforce:

- Consistent code formatting across languages
- Comprehensive linting for each technology
- Security vulnerability scanning
- Conventional commit message format: `type(scope): :emoji: description`
- Automated quality checks via pre-commit hooks
- CI/CD validation with GitHub Actions
