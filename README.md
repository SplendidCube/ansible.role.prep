# ansible.role.prep

Ansible preparation role for AWS infrastructure automation

## Overview

This Ansible role provides initial preparation and capability delivery for AWS infrastructure automation. It serves as a foundational role that should be included first in any playbook requiring AWS infrastructure provisioning.

## Prerequisites

- Python 3.11+
- AWS CLI configured with appropriate credentials (if AWS-related)
- Make
- Ansible 2.9+ (via package manager or virtual environment)
- Troposphere Python package (managed via Poetry)

## Quick Start

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/SplendidCube/ansible.role.prep.git
   cd ansible.role.prep
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
├── library/                 # Custom Ansible modules
│   ├── [custom_module].py   # Custom modules
│   ├── model_generate.py    # Main module for executing custom models
│   └── tests/               # Unit tests for modules
├── helpers/                 # Helper classes for module development
│   ├── base_model.py        # Generic base class for custom models
│   ├── [specific_helper].py # Specialized helper classes
│   └── troposphere_core.py  # CloudFormation template generation class
├── meta/                    # Ansible Galaxy metadata
│   └── main.yml             # Role metadata and dependencies
├── docs/                    # Sphinx documentation
│   ├── index.md             # Documentation entry point
│   ├── project-structure.md # Project structure guide
│   └── deployment.md        # Role usage and deployment guide
└── makefile                 # Development automation targets
```

## Capabilities

This role provides the following key capabilities:

1. **Infrastructure Preparation**: Automatic checks and validation before infrastructure deployment
2. **Custom Model Execution**: The `model_generate` module for executing custom Python models within Ansible
3. **Dynamic Path Management**: Adds the role directory to Python path for seamless module imports
4. **AWS Session Validation**: Ensures proper AWS credentials and session setup
5. **CloudFormation Integration**: Specialized support for Troposphere-based template generation

## Usage

### Basic Role Integration

Include the role in your playbook. Ensure the prepare role is the **first role** used by the playbook before any tasks are defined:

```yaml
---
- hosts: [target_hosts]
  roles:
    - ansible.role.prep  # Must be first
    - other.roles
  vars:
    # Role-specific variables
```

### Variables

Key variables that can be configured:

| Variable                   | Default | Description                                    |
| -------------------------- | ------- | ---------------------------------------------- |
| `aws_require_assumed_role` | `true`  | Require AWS role assumption for authentication |

### Custom Modules

The role includes the `model_generate` custom module:

```yaml
- model_generate:
    model: models/my_model
    description: My model
    parameters:
      param1: var1
```

### Advanced Configuration

#### Environment-Specific Settings

For different environments:

```yaml
# Development
ansible_role_prep_environment: dev
aws_require_assumed_role: false  # bypass AWS authentication

# Production  
ansible_role_prep_environment: prod
aws_require_assumed_role: true   # require role assumption
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
