# Deployment and Development Process

This document describes the development workflow and deployment process for `ansible.role.prep`, including setup, quality assurance, and technology-specific procedures.

## Overview

The development process uses:

- **Make**: Universal build system for all technologies
- **Pre-commit**: Automated quality checks and formatting
- **Conventional commits**: Standardized commit message validation
- **Technology-specific tools**: Poetry, Cargo, npm/yarn, etc.
- **Sphinx**: Documentation generation with MyST Markdown
- **GitHub Actions**: CI/CD validation workflow

## Development Workflow

### 1. Initial Setup

1. **Clone repository**: `git clone <repository-url>`
1. **Initialize environment**: `make init`
1. **Install pre-commit hooks**: `make pre-commit-install`
1. **Verify setup**: `make quality`

### 2. Development Process

1. **Create feature branch**: `git checkout -b feature/description`
1. **Make changes**: Edit code, tests, documentation
1. **Run quality checks**: `make quality` (includes lint, format, test)
1. **Commit changes**: Follow conventional commit format
1. **Push and create PR**: Standard GitHub workflow

### 3. Quality Assurance

All projects include comprehensive quality automation:

```bash
# Run all quality checks
make quality

# Individual checks
make lint           # Check code style and errors
make lint-fix       # Auto-fix linting issues
make format         # Format code
make format-check   # Check formatting without changes
make test           # Run test suite
```

### 4. Documentation

Generate and update documentation:

```bash
# Generate documentation
make docs

# View documentation locally
# Open docs/_build/html/index.html in browser
```

## Technology-Specific Workflows

### Python Projects

```bash
# Initialize Python environment
make init  # Creates virtualenv, installs dependencies via Poetry

# Quality checks
make lint       # Ruff linting
make format     # Ruff formatting
make type-check # MyPy type checking (if enabled)
make test       # pytest

# Development
poetry add package-name       # Add dependency
poetry add --group dev tool   # Add dev dependency
poetry shell                  # Activate environment
```

## Commit Message Format

All commits must follow the conventional format:

```text
type(scope): :emoji: description

feat(api): :sparkles: add user authentication endpoint
fix(ui): :bug: resolve navigation menu overflow issue
docs(readme): :memo: update installation instructions
```

**Types**: feat, fix, docs, style, refactor, test, chore, ci, build, perf, revert

**Scopes**: lowercase alphanumeric with hyphens

**Descriptions**: start with lowercase letter after emoji

## Pre-commit Hooks

Automated quality checks run on every commit:

- Code formatting (Ruff, rustfmt, Prettier)
- Linting (language-specific tools)
- Security scanning (Bandit for Python)
- Conventional commit validation
- File cleanup (trailing whitespace, end-of-file newlines)

## CI/CD Pipeline

GitHub Actions workflow (`validation.yml`) runs on every push:

- Environment setup for each technology
- Code quality checks
- Test execution
- Security scanning
- Documentation validation

## Troubleshooting

### Common Issues

1. **Pre-commit fails**: Run `make pre-commit-run` to see specific errors
1. **Dependencies outdated**: Technology-specific update commands
1. **Tests failing**: Check test output, update fixtures if needed
1. **Documentation build fails**: Check Sphinx configuration and MyST syntax

### Technology-Specific Troubleshooting

- **Python**: Check Poetry lock file, virtual environment activation
- **Rust**: Verify Rust toolchain, check Cargo.lock
- **JavaScript**: Clear node_modules, check package-lock.json
- **Ansible**: Verify ansible-lint configuration, role dependencies

## Best Practices

- **Run quality checks frequently**: Before commits, after major changes
- **Keep dependencies updated**: Regular maintenance of lock files
- **Write comprehensive tests**: Cover new features and bug fixes
- **Update documentation**: Keep README and docs/ current
- **Follow conventional commits**: Enables automated versioning and changelogs
- **Use make targets**: Consistent development experience across technologies

This process ensures reliable, maintainable, and well-documented projects with consistent quality across all supported technology stacks.
