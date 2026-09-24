# pre-commit-check-git-user

[![CI](https://github.com/grigoriev/pre-commit-check-git-user/actions/workflows/ci.yml/badge.svg)](https://github.com/grigoriev/pre-commit-check-git-user/actions/workflows/ci.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/grigoriev/pre-commit-check-git-user/badge)](https://scorecard.dev/viewer/?uri=github.com/grigoriev/pre-commit-check-git-user)
[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/14803/badge)](https://www.bestpractices.dev/projects/14803)
[![Release](https://img.shields.io/github/v/release/grigoriev/pre-commit-check-git-user)](https://github.com/grigoriev/pre-commit-check-git-user/releases)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=grigoriev_pre-commit-check-git-user&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=grigoriev_pre-commit-check-git-user)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=grigoriev_pre-commit-check-git-user&metric=coverage)](https://sonarcloud.io/summary/new_code?id=grigoriev_pre-commit-check-git-user)

Pre-commit hooks for validating Git user configuration. Ensure that `user.name` and `user.email` in your Git config match specified patterns before committing.

## Why?

When working across multiple projects (personal, work, open source), it's easy to accidentally commit with the wrong Git identity. These hooks help prevent that by validating your Git configuration against allowed patterns.

## Installation

Add to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/grigoriev/pre-commit-check-git-user
    rev: v0.9.4
    hooks:
      - id: check-git-config-user-email
        args: ["--templates", ".*@company\\.com$", ".*@personal\\.email$"]
      - id: check-git-config-user-name
        args: ["--templates", "^John Doe$", "^J\\.? Doe$"]
```

Then install:

```bash
pre-commit install
```

### Verify

GitHub releases after 0.9.3 carry a signed provenance bundle. Verify a downloaded file with
`gh attestation verify <file> --repo grigoriev/pre-commit-check-git-user`.

## Hooks

### check-git-config-user-email

Validates that `git config user.email` matches one of the provided regex templates.

```yaml
- id: check-git-config-user-email
  args: ["--templates", ".*@example\\.com$"]
```

Features:
- Validates email format before checking templates
- Supports multiple templates (matches if any one matches)
- Uses Python regex syntax

### check-git-config-user-name

Validates that `git config user.name` matches one of the provided regex templates.

```yaml
- id: check-git-config-user-name
  args: ["--templates", "^First Last$"]
```

## Examples

### Work project - only company email

```yaml
hooks:
  - id: check-git-config-user-email
    args: ["--templates", ".*@mycompany\\.com$"]
```

### Personal project - multiple allowed emails

```yaml
hooks:
  - id: check-git-config-user-email
    args: ["--templates", ".*@gmail\\.com$", ".*@protonmail\\.com$"]
```

### Validate full name format

```yaml
hooks:
  - id: check-git-config-user-name
    args: ["--templates", "^[A-Z][a-z]+ [A-Z][a-z]+$"]
```

## Development

### Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

### Setup

```bash
# Clone repository
git clone https://github.com/grigoriev/pre-commit-check-git-user.git
cd pre-commit-check-git-user

# Install dependencies
uv sync --all-extras
```

### Commands

```bash
# Run tests
uv run pytest tests/ -v

# Run tests with coverage
uv run pytest tests/ -v --cov=pre_commit_hooks --cov-report=term-missing

# Type checking
uv run mypy pre_commit_hooks

# Linting
uv run ruff check .

# Formatting
uv run ruff format .
```

### Project structure

```
├── pre_commit_hooks/
│   ├── __init__.py
│   ├── check_git_config_user_email.py
│   ├── check_git_config_user_name.py
│   └── py.typed
├── tests/
│   ├── test_check_git_config_user_email.py
│   └── test_check_git_config_user_name.py
├── .github/
│   ├── scripts/
│   │   ├── changelog-cut.sh
│   │   └── changelog-section.sh
│   └── workflows/
│       ├── bump-version.yml
│       ├── ci.yml
│       ├── release.yml
│       └── scorecard.yml
├── pyproject.toml
└── .pre-commit-hooks.yaml
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Disclaimer

This software is provided "as is", without warranty of any kind, as the LICENSE states. Use
it at your own risk. Sergey Grigoriev is not liable for damage from its use, as far as the law
allows. It is published free of charge, outside of any commercial offering, with no
obligation to support it. Security reports are welcome, see [SECURITY.md](SECURITY.md).

## License

MIT License - see [LICENSE](LICENSE) for details.
