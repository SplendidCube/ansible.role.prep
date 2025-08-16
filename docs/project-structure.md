# Project Structure

This document outlines the directory structure and key files in the `ansible.role.prep` project.

## Root Directory Structure

```text
ansible.role.prep/
├── README.md                        # Project overview and usage
├── makefile                         # Build and development targets
├── .editorconfig                    # Editor consistency settings
├── .gitignore                       # Git ignore patterns
├── .pre-commit-config.yaml          # Quality automation hooks
├── pyproject.toml                   # Poetry dependencies and configuration
├── docs/                            # Sphinx documentation
│   ├── conf.py
│   ├── index.md
│   ├── project-structure.md
│   ├── deployment.md
│   ├── _static/
│   └── _templates/
├── tasks/                           # Ansible role tasks
│   └── main.yml                     # Main role tasks
├── handlers/                        # Ansible handlers
├── vars/                            # Role variables
├── defaults/                        # Default variables
├── templates/                       # Jinja2 templates
├── files/                           # Static files
├── library/                         # Custom Ansible modules
│   ├── model_generate.py            # Main custom module
│   └── tests/                       # Unit tests
├── helpers/                         # Helper classes for module development
│   ├── base_model.py                # Generic base class
│   └── troposphere_core.py          # CloudFormation template generation
├── meta/                            # Ansible Galaxy metadata
│   └── main.yml                     # Role metadata and dependencies
└── tests/                           # Additional test files
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

### Ansible Projects

- **ansible-lint**: Role and playbook validation
- **molecule**: Testing framework (when applicable)

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
- **Editor consistency**: EditorConfig for all file types

## Quality Assurance

All projects enforce:

- Consistent code formatting across languages
- Comprehensive linting for each technology
- Security vulnerability scanning
- Conventional commit message format: `type(scope): :emoji: description`
- Automated quality checks via pre-commit hooks
- CI/CD validation with GitHub Actions
