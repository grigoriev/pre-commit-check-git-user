# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Security

- Harden the GitHub Actions workflows: least-privilege token permissions, no persisted
  checkout credentials, template values passed through `env:`.
- Add an actionlint and zizmor `lint` job to CI.
- Add the OpenSSF Scorecard workflow and badge.
- Let Renovate pin GitHub Actions by commit digest.
- Attach a signed build provenance bundle (`*.intoto.jsonl`) to each GitHub release.

### Changed

- Run CI once per commit on Renovate branches: drop `renovate/**` from the push trigger
  and the `create-pr-on-failure` job that served it.
- Create the GitHub release with `gh release create` instead of a third-party action.

### Added

- Disclaimer section in the README.

Earlier releases are listed on the
[GitHub releases page](https://github.com/grigoriev/pre-commit-check-git-user/releases).
