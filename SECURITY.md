# Security policy

## Reporting a vulnerability

Report a vulnerability privately through GitHub:
https://github.com/grigoriev/pre-commit-check-git-user/security/advisories/new
(the **Security** tab, **Report a vulnerability**). Do not open a public issue for it.

We answer within a week. The fix goes into the next release, and its release notes name it.

## Supported versions

Only the latest release gets fixes.

## Scope

The hooks in `pre_commit_hooks/`, the hook definitions in `.pre-commit-hooks.yaml`, the
scripts and the workflows belong to this repository.

Vulnerabilities in upstream software (Python, Git, pre-commit and the development tools) belong
to the upstream project. Tell us as well if this project is affected, so we can release a fix
when the upstream fix is out.
