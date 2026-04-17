## ADDED Requirements

### Requirement: Automated versioning from conventional commits
The repository SHALL use release-please to analyze conventional commits pushed to `main` and automatically determine the next semantic version. The release type SHALL be `simple`. The initial version SHALL be `1.0.0`.

#### Scenario: Feature commit triggers minor version bump
- **WHEN** a commit with prefix `feat:` is pushed to `main`
- **THEN** release-please opens or updates a release PR bumping the minor version (e.g., 1.0.0 -> 1.1.0)

#### Scenario: Fix commit triggers patch version bump
- **WHEN** a commit with prefix `fix:` is pushed to `main`
- **THEN** release-please opens or updates a release PR bumping the patch version (e.g., 1.0.0 -> 1.0.1)

#### Scenario: Breaking change triggers major version bump
- **WHEN** a commit with `BREAKING CHANGE` footer or `!` after the type is pushed to `main`
- **THEN** release-please opens or updates a release PR bumping the major version (e.g., 1.0.0 -> 2.0.0)

#### Scenario: Non-conventional commit has no effect
- **WHEN** a commit without a conventional commit prefix is pushed to `main`
- **THEN** release-please does not include that commit in the changelog or version calculation

### Requirement: Automated changelog generation
The repository SHALL maintain a `CHANGELOG.md` file that is automatically updated by release-please. Changelog sections SHALL include: Features, Bug Fixes, Miscellaneous, Documentation, and Refactoring.

#### Scenario: Changelog updated on release PR merge
- **WHEN** a release-please PR is merged
- **THEN** `CHANGELOG.md` is updated with grouped entries for all commits since the last release

#### Scenario: Changelog sections map to commit types
- **WHEN** the changelog is generated
- **THEN** `feat:` commits appear under "Features", `fix:` under "Bug Fixes", `chore:` under "Miscellaneous", `docs:` under "Documentation", and `refactor:` under "Refactoring"

### Requirement: GitHub Release creation
The repository SHALL create a GitHub Release with a git tag when a release-please PR is merged.

#### Scenario: Release created on PR merge
- **WHEN** the release-please PR is merged to `main`
- **THEN** a GitHub Release is created with the version tag (e.g., `v1.1.0`) and release notes from the changelog

### Requirement: Release workflow configuration
The release workflow SHALL be defined in `.github/workflows/ci_release.yml`. It SHALL use the `googleapis/release-please-action` pinned by SHA. It SHALL set workflow-level `permissions: {}` and grant `contents: write` and `pull-requests: write` at the job level.

#### Scenario: Workflow triggers on push to main
- **WHEN** a commit is pushed to the `main` branch
- **THEN** the `ci_release.yml` workflow runs

#### Scenario: Workflow does not trigger on other branches
- **WHEN** a commit is pushed to a branch other than `main`
- **THEN** the `ci_release.yml` workflow does not run

### Requirement: Release-please configuration files
The repository SHALL contain `release-please-config.json` and `.release-please-manifest.json` at the repository root. The config SHALL specify `simple` release type, disable component in tag, and define changelog sections. The manifest SHALL track the current version.

#### Scenario: Config file structure
- **WHEN** `release-please-config.json` is read
- **THEN** it contains a `packages` key with `"."` entry specifying `release-type: "simple"`, `include-component-in-tag: false`, and `changelog-sections` array

#### Scenario: Manifest tracks current version
- **WHEN** `.release-please-manifest.json` is read
- **THEN** it contains `{".": "<current-version>"}` where the initial value is `"1.0.0"`
