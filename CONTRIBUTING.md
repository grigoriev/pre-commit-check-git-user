# Contributing

Thanks for your interest in improving this project.

## Development

This project uses [uv](https://docs.astral.sh/uv/). Run the checks with:

```sh
uv run ruff check .
uv run mypy .
uv run pytest
```

## Commit messages

This project follows [Conventional Commits](https://www.conventionalcommits.org/):
`type: subject`, imperative mood, lowercase first letter, no trailing period,
subject under 50 characters. Types: `feat`, `fix`, `docs`, `style`, `refactor`,
`perf`, `test`, `build`, `ci`, `chore`.

## Style

- American spelling.
- One idea per sentence, active voice.
- Keep changes minimal and focused on the task.
- Do not use em dashes.

## Before opening a pull request

- Run the checks above and make sure CI is green.
