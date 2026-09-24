# Contributing

Issues and pull requests are welcome.

## Build and test

```sh
uv sync --all-extras                # install the dependencies
uv run ruff check .                 # lint
uv run ruff format --check .        # format check
uv run mypy pre_commit_hooks tests  # type check
uv run pytest tests/ --cov          # tests with coverage
uv build                            # wheel and sdist
```

CI runs actionlint, zizmor, ruff, mypy, the tests on Python 3.11 to 3.14 and SonarCloud for
every pull request.

## Pull requests

1. Branch from the default branch as `type/description`, for example `fix/empty-title`.
2. Keep one change per pull request. New behavior comes with tests; a bug fix adds a test that
   fails without it.
3. Write commit messages as [Conventional Commits](https://www.conventionalcommits.org/) without a
   scope: `feat: ...`, `fix: ...`, `docs: ...`, `refactor: ...`, `test: ...`, `build: ...`,
   `ci: ...`, `chore: ...`.
4. Sign your commits. The default branch accepts verified signatures only.
5. Add an entry under `## [Unreleased]` in `CHANGELOG.md`, written for users: the release notes
   quote it. Update the README when behavior or configuration changes.

Pull requests are squash-merged once all required checks are green.

## Releases

A maintainer runs the Bump Version workflow. It moves the Unreleased entries into a versioned
section, tags the release, and the Release workflow publishes it with signed build provenance.
