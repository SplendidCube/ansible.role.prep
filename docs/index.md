# Ansible Role :: Prep

Welcome to the documentation for `ansible.role.prep`. This Ansible role provides initial preparation and capability delivery for AWS infrastructure automation.

## Overview

This project provides:

- **Infrastructure Preparation**: Automatic checks and validation before infrastructure deployment
- **Custom Model Execution**: The `model_generate` module for executing custom Python models within Ansible
- **AWS Integration**: Session validation and authentication management for AWS infrastructure

## Quick Start

1. **Prerequisites**:
   - Python 3.11+
   - AWS CLI
   - Make
   - Ansible 2.9+
   - Troposphere
1. **Initialize Environment**: `make init`
1. **Run Quality Checks**: `make quality`
1. **Generate Documentation**: `make docs`

## Documentation Structure

```{toctree}
:maxdepth: 2
:caption: Contents:

project-structure
deployment
src
```

## Project Information

- **Repository**: ansible.role.prep (Private)
- **Owner**: SplendidCube
- **Technology Stack**:
  - Ansible
  - Python
  - Troposphere
  - AWS CloudFormation
- **License**: Proprietary

## Development

For development setup and contribution guidelines, see the [project structure](project-structure.md) documentation.

## Support

This is a private project managed by SplendidCube. For questions or issues, refer to internal documentation or contact the maintainers.

## Indices and Tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
