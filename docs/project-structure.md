# Project Structure

This document outlines the directory structure and key files in the `ansible.role.prep` project.

## Root Directory Structure

```text
/
├── .github/                     # GitHub repository settings and Workflows
│   ├── workflows/               # Workflow definitions
│   │   ├── validate.yml         # Basic validation checks workflow
│   │   └── deploy-[TEMPLATE: env | kebab-case].yml # Deployment Workflow for promoting the project to [TEMPLATE: env | kebab-case] environment
│   ├── copilot-instructions.md  # Copilot INSTRUCTIONS for the project
│   ├── pull_request_template.md # Template for PR description in GitHub
│   └── settings.yml             # GitHub repository settings
├── .vscode/                     # VSCode local environment settings
│   ├── extensions.json          # Recommended plugins for this project
│   └── settings.json            # Project-specific settings for this project
├── docs/                        # Sphinx documentation (MyST Markdown)
│   ├── _static/                 # Static assets (logo.svg, custom.css)
│   ├── _templates/              # Custom Sphinx templates
│   ├── conf.py                  # Sphinx config (Wagtail theme, SplendidCube branding)
│   ├── index.md                 # Documentation entry page (table of contents)
│   ├── project-structure.md     # Project layout and descriptions
│   └── deployment.md            # Deployment and CI/CD guidance
├── helpers/                     # Helper classes for module development
│   ├── aws_resource_model.py    # AWS resource modeling base class
│   └── cfn_builder.py           # CloudFormation template generation
├── library/                     # Custom Ansible modules
│   ├── generate_model.py        # Main custom module
│   └── tests/                   # Unit tests
├── meta/                        # Ansible Galaxy metadata
│   └── main.yml                 # Role metadata and dependencies
├── tasks/                       # Ansible role tasks
│   └── main.yml                 # Main role tasks
├── tests/                       # Test files
├── .ansible-lint                # Ansible lint configuration
├── .editorconfig                # Editor consistency settings
├── .gitignore                   # Git ignore patterns
├── .pre-commit-config.yaml      # Quality automation hooks
├── .secrets.baseline            # Configuration to prevent secrets being committed to the repository
├── .venv                        # VirtualEnv project name for easy identification
├── LICENSE                      # Project license information
├── makefile                     # Build and development targets
├── pyproject.toml               # Python Project settings for Ansible/Python scripts
└── README.md                    # Project overview and usage
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
