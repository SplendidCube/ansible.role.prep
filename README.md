# Project Name

Ansible role template for SplendidCube infrastructure automation

## Overview

This Ansible role provides [role-specific functionality description]. It serves as a [foundational/specialized/utility] role for [specific use case or infrastructure components].

## Prerequisites

- Python 3.11+
- AWS CLI configured with appropriate credentials (if AWS-related)
- Make
- Ansible 2.9+ (`pip install ansible` or system package manager)
- [Additional role-specific prerequisites]

## Quick Start

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <project-name>
   ```

1. Initialize the development environment:

   ```bash
   make init
   ```

1. Install dependencies:

   ```bash
   make install
   ```

### Development

- **Quality checks**: `make quality` (linting + formatting + ansible-lint)
- **Testing**: `make test` (pytest + ansible syntax checking)
- **Documentation**: `make docs`
- **Pre-commit setup**: `make pre-commit-install`

### Common Commands

```bash
make help              # Show all available commands
make init              # Initialize development environment
make install           # Install dependencies
make dev               # Install development dependencies
make lint              # Run linting checks (Python + Ansible)
make lint-fix          # Fix auto-fixable issues
make format            # Format code
make test              # Run tests
make test-coverage     # Run tests with coverage
make ansible-syntax    # Check Ansible syntax
make docs              # Generate documentation
make clean             # Clean up environment
```

## Project Structure

```text
├── tasks/                   # Ansible role tasks
│   └── main.yml             # Main role tasks
├── handlers/                # Ansible handlers (if needed)
├── vars/                    # Role variables
├── defaults/                # Default variables
├── templates/               # Jinja2 templates (if needed)
├── files/                   # Static files (if needed)
├── library/                 # Custom Ansible modules (if needed)
│   ├── [custom_module].py   # Custom modules
│   └── tests/               # Unit tests for modules
├── helpers/                 # Helper classes for module development (if needed)
│   ├── base_model.py        # Generic base class for custom models
│   └── [specific_helper].py # Specialized helper classes
├── meta/                    # Ansible Galaxy metadata
│   └── main.yml             # Role metadata and dependencies
├── docs/                    # Sphinx documentation
│   ├── index.md             # Documentation entry point
│   ├── project-structure.md # Project structure guide
│   └── deployment.md        # Role usage and deployment guide
└── makefile                 # Development automation targets
```

## Capabilities

This template provides the following key capabilities:

1. **[Primary Capability]**: [Description of main functionality]
1. **[Secondary Capability]**: [Description of additional functionality]
1. **[Additional Features]**: [Any special features or integrations]

## Usage

### Basic Role Integration

Include the role in your playbook:

```yaml
---
- hosts: [target_hosts]
  roles:
    - [role_name]
  vars:
    # Role-specific variables
```

### Variables

Key variables that can be configured:

| Variable          | Default           | Description   |
| ----------------- | ----------------- | ------------- |
| `[variable_name]` | `[default_value]` | [Description] |

### Custom Modules (if applicable)

If the role includes custom modules, document their usage:

```yaml
- [module_name]:
    parameter: value
    description: "Module description"
```

### Advanced Configuration

#### Environment-Specific Settings

For different environments:

```yaml
# Development
[role_name]_environment: dev

# Production
[role_name]_environment: prod
```

## Contributing

1. Ensure all quality checks pass: `make quality`
1. Run tests: `make test`
1. Update documentation as needed
1. Follow established patterns for tasks, handlers, and custom modules
1. Test role in isolation and with dependent roles

## Development Standards

This project follows SplendidCube organizational standards:

- **Code Quality**: Automated linting and formatting
- **Testing**: Comprehensive test coverage
- **Documentation**: Clear and maintainable docs
- **Consistency**: Standardized tooling and workflows

For detailed development guidelines, see the [Copilot Instructions](.github/copilot-instructions.md).
