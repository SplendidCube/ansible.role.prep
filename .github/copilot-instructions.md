# Copilot & AI Assistant Instructions

**READ THIS FIRST** - This file contains important project conventions, preferences, and standards for AI assistants working on this project. Always reference this file to ensure consistency with established patterns and user preferences.

## Project Overview

- **Repository**: [ROLE_NAME] (Ansible role for [role purpose])
- **Owner**: SplendidCube
- **Type**: **PRIVATE PROJECT** - Do not publish or share publicly
- **Main Branch**: `master`
- **Project Type**: Ansible Role with Python modules and helper classes
- **Purpose**: [Brief role purpose description - infrastructure automation, configuration management, etc.]

## User Preferences & Standards

### Documentation Philosophy

- **Core information consolidated in `README.md`** for quick reference
- **Detailed documentation allowed in `docs/` folder** for comprehensive guides (Sphinx with SplendidCube branding)
- **Professional SplendidCube branding** integrated into all documentation with logo and navy blue theme
- **Automated Markdown formatting** via pre-commit hooks (mdformat)
- Keep documentation concise and directly relevant
- Avoid verbose explanations or redundant information between README and docs

### GitHub Repository Configuration

- **Repository is PRIVATE**
- **Issues and Projects are DISABLED** - user doesn't want to use GitHub for these features
- **Downloads are DISABLED**
- **Wiki is DISABLED**
- Only use GitHub for code, PRs, and CI/CD

### Branch Structure & Workflows

- **master**: Production branch with strict protection rules
- **development**: Primary development branch with relaxed protection for active development
- **Feature branches**: Created from master, merged to development via PR
- **Workflow**: master → feature-branch → development (PR) → master (PR after testing and review; final master PR merge performed by repository owner or designated maintainer after successful CI checks and user validation))
- **Simple CI/CD workflows** focused on quality and testing
- No complex deployment workflows unless specifically required

### Git & Version Control Preferences

- **User handles git commits** - Do not perform git commits, adds, or pushes unless explicitly requested
- **AI assistants should make file changes** but leave version control operations to user
- **Exception**: Only perform git operations when user explicitly asks (e.g., "commit these changes")
- **Branch workflow**: Create feature branches from master, PR to development, then PR to master after testing
- **Keep master clean**: All development work happens in feature branches and development branch
- **Focus on file modifications** rather than version control workflow management

### Development Environment

- **Make**: Primary build and task automation tool
- **Poetry**: Dependency management for Python modules and helper classes
- **uvx**: Fast tool execution without environment overhead for Python tools
- **Virtual environments stored centrally** in `~/.virtualenvs/` via virtualenvwrapper
- **Auto-activation** based on `.venv` file in project root
- **EditorConfig**: Consistent editor settings across environments (`.editorconfig`)
- **Pre-commit**: Automated quality checks and formatting
- **Comprehensive toolchain support**:
  - Python: Poetry, Ruff, pytest, MyPy, Sphinx
  - Ansible: ansible-lint, role validation
  - General: conventional commits validation
- Ansible-specific makefile with standard targets: `init`, `lint`, `format`, `test`, `docs`, `quality`

### Code Quality Standards

- **Consistent tooling** across all projects and technology stacks
- **Pre-commit hooks** for automated quality checks and enforcement
- **Linting and formatting** enforced automatically for all supported languages
- **Conventional commits** with strict validation enforcing user's preferred format:
  - Format: `type(scope): :emoji: description`
  - Types: feat, fix, docs, style, refactor, test, chore, ci, build, perf, revert
  - Scopes: lowercase alphanumeric with hyphens
  - Descriptions: must start with lowercase letter after emoji
- **Security scanning** with Bandit for Python and other security tools
- **Testing** as a standard requirement with coverage expectations
- **Documentation** kept up-to-date and relevant
- **Docstring formatting** with mandatory structural line breaks:
  - **REQUIRED**: Use triple-quote format with line breaks: `"""\nContent\n"""`
  - **AVOID**: Inline format without line breaks: `"""Content"""`
  - **Standard**: reStructuredText (reST) format for optimal Sphinx integration
  - **Parameters**: Use `:param name: description` and `:type name: TypeName`
  - **Returns**: Use `:returns: description` and `:rtype: TypeName`
  - **Examples**: Use `Example::` with proper indentation for code blocks
  - **No manual line breaks in content**: Let IDE handle wrapping of docstring text naturally

### File Structure Preferences

```text
.vscode/
└── settings.json          # VS Code configuration

.github/
├── copilot-instructions.md # This file
└── workflows/             # CI/CD workflows (if needed)

makefile                   # Development automation
.editorconfig             # Editor consistency
.gitignore                # Comprehensive ignore patterns
.pre-commit-config.yaml   # Quality automation
README.md                 # Consolidated documentation
docs/                     # Detailed documentation (with SplendidCube branding)
├── _static/
│   ├── logo.svg         # SplendidCube professional logo
│   └── custom.css       # Professional navy blue theme
├── conf.py              # Sphinx configuration with branding
├── index.md             # Main documentation page
└── *.md                 # Additional documentation pages
```

## Development Standards

### Makefile Requirements

**MUST include comprehensive targets**:

- `init`: Environment setup and dependency installation (technology-agnostic)
- `install`: Install production dependencies
- `dev`: Install development dependencies
- `lint`: Run linting checks across all relevant technologies
- `lint-fix`: Auto-fix linting issues where possible
- `format`: Format code for all supported languages
- `format-check`: Check code formatting without modification
- `test`: Run tests with appropriate test runners
- `docs`: Generate documentation (Sphinx, mdbook, etc.)
- `pre-commit-install`: Install pre-commit hooks
- `pre-commit-run`: Run pre-commit on all files
- `pre-commit-staged`: Run pre-commit on staged files only
- `quality`: Run all quality checks (lint + format + test)
- `clean`: Cleanup environment and build artifacts
- `help`: Show available targets with descriptions

**Technology-specific patterns**:

- Python: Poetry for dependencies, uvx for tools, Ruff for quality
- Rust: Cargo for all operations, clippy for linting
- JavaScript/TypeScript: npm/yarn for dependencies, ESLint/Prettier for quality
- Ansible: ansible-lint for validation
- Docker: hadolint for Dockerfile linting

### Ansible Role Standards

- **Role should be first** in any playbook using it
- **Automatic execution** of preparation tasks on role inclusion
- **Custom modules** in `library/` directory
- **Helper classes** in `helpers/` directory for model development
- **Comprehensive testing** with fixtures in `tests/` directory
- **Galaxy metadata** properly configured in `meta/main.yml`

### Quality Assurance

- **Automated formatting** via pre-commit hooks
- **Consistent linting** across projects and technologies
- **Security scanning** integrated into quality checks
- **Conventional commits** enforced with specific format validation
- **Test coverage** requirements maintained
- **Documentation standards** consistently applied
- **CI/CD validation** with GitHub Actions workflow

## Quality Assurance Notes

### Always Remember

1. **Check existing file contents** before making edits
1. **Consolidate documentation** in README.md for core information
1. **Use absolute paths** for reliability in scripts
1. **Test thoroughly** before considering tasks complete
1. **Respect user's preference** for minimal GitHub features
1. **Never suggest tools or alternatives unless explicitly asked**
1. **Avoid verbose explanations or unsolicited recommendations**
1. **Focus on requested changes** rather than suggesting improvements

### Common Patterns

- Standard makefile targets across all projects and technology stacks
- Consistent VS Code settings for team development with comprehensive language support
- Pre-commit hooks for comprehensive quality automation across all technologies
- Clear separation between core docs (README) and detailed docs (docs/)
- EditorConfig for consistent code formatting across editors and IDEs
- Conventional commits with strict format validation
- GitHub Actions validation.yml workflow for CI/CD consistency
- Security scanning and vulnerability detection integrated into development workflow

### Avoid

- Creating separate documentation files for basic information (use README.md)
- Using GitHub issues/projects (disabled by user preference)
- Using relative paths in scripts and automation
- Overly verbose explanations in responses
- **Suggesting irrelevant tools or alternatives** - stick to established patterns
- **Recommending tools not explicitly requested** - avoid unsolicited suggestions
- Breaking established project patterns without clear justification
- **Inline docstring format** - always use line-break style: `"""\nContent\n"""`
- **Non-reST docstring formats** - use reStructuredText for Sphinx compatibility
- **Manual line breaks in docstring content** - let IDE handle natural text wrapping

## Project-Specific Notes

**Template Usage Instructions**:

1. **Copy template files** to new project directory
1. **Update project-specific placeholders**:
   - Replace `[PROJECT_NAME]` with actual project name
   - Replace `[Brief description]` with project description
   - Replace `[Fill in: ...]` with appropriate project type and purpose
1. **Remove unused technology configurations**:
   - Delete unused language sections from makefile
   - Remove unused hooks from .pre-commit-config.yaml
   - Clean .gitignore for only relevant technologies
1. **Install dependencies** based on project technology stack
1. **Run `make init`** to set up development environment
1. **Run `make pre-commit-install`** to enable quality automation

**Technology Support**:

- Python: Full Poetry, Ruff, pytest, MyPy, Sphinx with SplendidCube branding support
- Rust: Cargo, clippy, rustfmt integration
- JavaScript/TypeScript: ESLint, Prettier, comprehensive linting
- Ansible: ansible-lint validation
- Docker: hadolint for Dockerfile quality
- Markdown: mdformat for consistent documentation formatting

**Documentation Branding**:

- Professional SplendidCube logo integration (logo.svg)
- Navy blue color scheme (#1e3a8a primary, #3b82f6 secondary)
- Custom CSS with both light and dark mode support
- Clean syntax highlighting for code blocks
- Professional form styling and consistent branding
- Edit button removal for cleaner interface

**Quality Automation**:

- All commits automatically validated for conventional format
- Code formatting enforced across all supported languages
- Security vulnerabilities scanned on every commit
- Documentation consistency maintained automatically

## Update History

- 2025-08-15: Initial template creation based on SplendidCube organizational standards
- 2025-08-15: Added comprehensive multi-technology support (Python, Rust, JavaScript/TypeScript, Ansible, Docker)
- 2025-08-15: Integrated EditorConfig for consistent editor settings across all environments
- 2025-08-15: Implemented comprehensive pre-commit automation with conventional commits validation
- 2025-08-15: Added security scanning (Bandit, semgrep) and vulnerability detection
- 2025-08-15: Created comprehensive makefile with technology-agnostic targets
- 2025-08-15: Established GitHub Actions validation.yml workflow for CI/CD consistency
- 2025-08-15: Added comprehensive VS Code settings for all supported languages
- 2025-08-16: Integrated comprehensive SplendidCube documentation branding with logo and professional navy blue theme
- 2025-08-16: Established docstring formatting standards with mandatory line breaks and reST format
- 2025-08-16: Added code quality best practices for helper classes and abstract base classes
- 2025-08-16: Implemented systematic class naming improvements (BaseModel→AwsResourceModel, TroposphereCore→CfnBuilder)
- 2025-08-16: Added comprehensive error handling patterns and type hint standards for Ansible integration
