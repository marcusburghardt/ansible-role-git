## ADDED Requirements

### Requirement: Automated Galaxy publishing on release
The repository SHALL automatically publish the role to Ansible Galaxy when a GitHub Release is published. The workflow SHALL be defined in `.github/workflows/ci_galaxy_publish.yml`.

#### Scenario: Role imported on release publish
- **WHEN** a GitHub Release event with type `published` occurs
- **THEN** the workflow runs `ansible-galaxy role import` with the repository owner and name

#### Scenario: Workflow does not run on other events
- **WHEN** a push to `main` or PR merge occurs without a release event
- **THEN** the `ci_galaxy_publish.yml` workflow does not trigger

### Requirement: Galaxy API authentication
The workflow SHALL authenticate to Ansible Galaxy using the `GALAXY_API_KEY` repository secret. The secret value MUST NOT be hardcoded in the workflow file.

#### Scenario: Successful authentication
- **WHEN** the `GALAXY_API_KEY` secret is configured in repository settings
- **THEN** the `ansible-galaxy role import` command authenticates successfully

#### Scenario: Missing API key
- **WHEN** the `GALAXY_API_KEY` secret is not configured
- **THEN** the workflow fails with an authentication error

### Requirement: Workflow security
The Galaxy publish workflow SHALL set workflow-level `permissions: {}` and grant only `contents: read` at the job level. All third-party actions SHALL be pinned by full SHA.

#### Scenario: Minimal permissions
- **WHEN** the workflow runs
- **THEN** it has only `contents: read` permission at the job level

### Requirement: Python and ansible-core setup
The workflow SHALL set up Python 3.12 and install a pinned version of `ansible-core` before running the Galaxy import command.

#### Scenario: Deterministic environment
- **WHEN** the workflow installs dependencies
- **THEN** `ansible-core` is installed at a specific pinned version (e.g., `ansible-core==2.17.8`)
