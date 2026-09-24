# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Releases before 0.9.4 are listed on the
[GitHub releases page](https://github.com/grigoriev/pre-commit-check-git-user/releases).

## [Unreleased]

### Changed

- The version bump moves the Unreleased entries of this changelog into a section for
  the new version. The GitHub release takes its notes from that section.
- Align the repository with the shared baseline: workflow values reach `run:` through
  `env:`, CI jobs have time limits, the version bump pushes without stored credentials,
  a release run fails when the release exists already, SonarCloud analyzes the tests as
  tests, and the author email is `grigoriev@fastmail.com`.

## [0.9.4] - 2026-09-24

### Security

- Harden the GitHub Actions workflows: least-privilege token permissions, no persisted
  checkout credentials, template values passed through `env:`.
- Add an actionlint and zizmor `lint` job to CI.
- Add the OpenSSF Scorecard workflow and badge.
- Let Renovate pin GitHub Actions by commit digest.
- Attach a signed build provenance bundle (`*.intoto.jsonl`) to each GitHub release.
- Update pygments to 2.21.0 (PYSEC-2026-2987, ReDoS). It is a test dependency only.
- Let Renovate refresh the lock file weekly and open PRs for known vulnerabilities in it.

### Changed

- Run CI once per commit on Renovate branches: drop `renovate/**` from the push trigger
  and the `create-pr-on-failure` job that served it.
- Create the GitHub release with `gh release create` instead of a third-party action.
- Renovate takes its common rules from the shared preset `github>grigoriev/renovate-config`.

### Added

- Disclaimer section in the README.

### Fixed

- A rerun of the release workflow uploads the files to the existing release
  instead of failing.
