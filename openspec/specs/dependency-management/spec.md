## ADDED Requirements

### Requirement: Dependabot monitors GitHub Actions
The repository SHALL configure Dependabot to monitor the `github-actions` package ecosystem for dependency updates on a weekly schedule. The configuration SHALL be defined in `.github/dependabot.yml`.

#### Scenario: Weekly action update check
- **WHEN** the weekly Dependabot schedule runs
- **THEN** Dependabot checks for newer versions of all GitHub Actions used in workflow files

#### Scenario: Update PR created
- **WHEN** a newer version of a GitHub Action is available
- **THEN** Dependabot opens a PR updating the SHA pin and version comment

### Requirement: Conventional commit format for Dependabot
Dependabot commit messages SHALL use the `chore` prefix with scope included, following the Conventional Commits specification.

#### Scenario: Commit message format
- **WHEN** Dependabot creates an update PR
- **THEN** the commit message uses the format `chore(deps): bump <action> from <old> to <new>`
