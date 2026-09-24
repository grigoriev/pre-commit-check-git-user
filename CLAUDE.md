# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/claude-code) when working with this repository.

## Project Overview

This is a Python package providing pre-commit hooks for validating Git user configuration (`user.name` and `user.email`). It ensures commits are made with the correct identity by matching against regex patterns.

## Tech Stack

- **Python**: 3.11+
- **Package Manager**: uv
- **Build Backend**: hatchling
- **Linting/Formatting**: ruff
- **Type Checking**: mypy (strict mode)
- **Testing**: pytest with pytest-cov

## Common Commands

```bash
# Install dependencies
uv sync --all-extras

# Run all checks (what CI does)
uv run ruff check .
uv run ruff format --check .
uv run mypy pre_commit_hooks
uv run pytest tests/ -v

# Fix linting/formatting issues
uv run ruff check --fix .
uv run ruff format .

# Run tests with coverage
uv run pytest tests/ -v --cov=pre_commit_hooks --cov-report=term-missing

# Build package
uv build
```

## Architecture

### Hooks

Two independent hooks in `pre_commit_hooks/`:

1. **check_git_config_user_email.py**
   - Validates `git config user.email`
   - Checks email format with `EMAIL_PATTERN` before template matching
   - Entry point: `main(argv: Sequence[str] | None = None) -> int`

2. **check_git_config_user_name.py**
   - Validates `git config user.name`
   - Entry point: `main(argv: Sequence[str] | None = None) -> int`

Both hooks:
- Accept `--templates` argument with one or more regex patterns
- Return 0 on success, 1 on failure
- Use `re.match()` (matches from start of string)

### Configuration

- `.pre-commit-hooks.yaml`: Hook definitions for pre-commit framework
- `pyproject.toml`: Package metadata, dependencies, tool configs

## Code Style

- Strict mypy typing required
- All functions must have type annotations
- Use `from __future__ import annotations` for modern syntax
- Import `Sequence` from `collections.abc`, not `typing`
- Use f-strings for string formatting
- Keep functions small and focused

## Testing

Tests use pytest with `unittest.mock` for subprocess mocking:

```python
@patch("pre_commit_hooks.check_git_config_user_name.subprocess.run")
def test_example(self, mock_run):
    mock_run.return_value = MagicMock(stdout="value\n", returncode=0)
    result = main(["--templates", "pattern"])
    assert result == 0
```

## CI/CD

- **CI** (`ci.yml`): Runs on push/PR to main
  - Lint job: actionlint and zizmor audit the workflows
  - Tests on Python 3.11, 3.12, 3.13, 3.14
  - Linting, type checking, tests, build

- **Scorecard** (`scorecard.yml`): OpenSSF Scorecard, weekly and on push to main

- **Workflow security**: every workflow sets top-level `permissions`, `${{ }}` values
  reach `run:` through `env:`, and every action is pinned by commit SHA. Checkouts use
  `persist-credentials: false`. Only the bump-version checkout keeps the PAT credentials,
  because its Commit and tag step pushes with them

- **Release** (`release.yml`): Runs on `v*` tags
  - Runs tests
  - Creates GitHub release with the wheel, the sdist and a signed provenance bundle
    (`actions/attest-build-provenance`, `*.intoto.jsonl`)

## Release Process

1. Update version in `pyproject.toml`
2. Commit changes
3. Create and push tag:
   ```bash
   git tag v0.9.2
   git push origin v0.9.2
   ```
4. GitHub Actions creates the GitHub release. The package is not published to PyPI
