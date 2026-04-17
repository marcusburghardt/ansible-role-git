## Why

The role has no CI/CD pipeline, no automated release process, and is missing standard project hygiene files (`.gitignore`, `.yamllint`, `LICENSE`). Releases to Ansible Galaxy are manual, there is no changelog, and YAML linting has no enforced standard. The `ansible-role-ai` sibling role already has this infrastructure working well via release-please and GitHub Actions, so we can replicate a proven pattern rather than inventing from scratch.

## What Changes

- Add GitHub Actions workflow for automated release management via release-please (conventional commits drive versioning, changelog generation, and GitHub Releases).
- Add GitHub Actions workflow for automated Ansible Galaxy publishing triggered by GitHub Releases.
- Add Dependabot configuration for weekly GitHub Actions dependency updates.
- Add release-please configuration files (manifest at v1.0.0, config with `simple` release type).
- Add root `.gitignore` for OpenSpec/OpenCode framework artifacts and agent tool directories.
- Add `.yamllint` configuration for consistent YAML linting standards.
- Add `LICENSE` file with Apache-2.0 full text (aligning with `ansible-role-ai`).
- Add `CHANGELOG.md` initial file (release-please will manage it going forward).
- **BREAKING**: License change from MPL-2.0 to Apache-2.0. Update `meta/main.yml` and `README.md` to reflect the new license.

## Capabilities

### New Capabilities
- `release-automation`: Automated versioning, changelog generation, and GitHub Release creation via release-please and GitHub Actions.
- `galaxy-publishing`: Automated Ansible Galaxy role publishing triggered by GitHub Releases.
- `dependency-management`: Dependabot configuration for keeping GitHub Actions dependencies up to date.
- `project-hygiene`: Root `.gitignore`, `.yamllint`, and `LICENSE` files establishing baseline project standards.

### Modified Capabilities

(No existing specs to modify -- the `openspec/specs/` directory is empty.)

## Impact

- **Repository root**: 9 new files added, 2 existing files updated (`meta/main.yml`, `README.md`).
- **License**: Changes from MPL-2.0 to Apache-2.0. All downstream consumers should be aware.
- **Developer workflow**: Commits to `main` must follow Conventional Commits format for release-please to function correctly.
- **Dependencies**: Introduces GitHub Actions dependencies (`googleapis/release-please-action`, `actions/checkout`, `actions/setup-python`) and `ansible-core` as a CI dependency for Galaxy publishing.
