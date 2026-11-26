## ADDED Requirements

### Requirement: Package installation is an independent task

The role SHALL install the OS packages required for Git workflows through a
task named `install_packages` that is independently selectable in `git_tasks`.

#### Scenario: Package task enabled

- **WHEN** `install_packages` is enabled in `git_tasks`
- **THEN** the role ensures the packages from the OS-specific package list are
  present

#### Scenario: Package task disabled

- **WHEN** `install_packages` is disabled or omitted from `git_tasks`
- **THEN** the role does not invoke the system package manager

### Requirement: Only package installation escalates privileges

The `install_packages` task SHALL be the only role task that uses privilege
escalation. All user-scoped configuration tasks SHALL run without `become`.

#### Scenario: Configuration without a sudo password

- **WHEN** a playbook runs `configure_git` with `install_packages` disabled and
  no become password is supplied
- **THEN** the task completes without attempting privilege escalation

#### Scenario: Package installation escalates

- **WHEN** `install_packages` runs and packages are missing
- **THEN** only that task requests privilege escalation to install them

### Requirement: Default task order installs packages first

The default `git_tasks` list SHALL place `install_packages` before tasks that
invoke the `git` binary, so a default run satisfies tool dependencies first.

#### Scenario: Default order

- **WHEN** a user runs the role without overriding `git_tasks`
- **THEN** package installation is attempted before repository synchronization
  and Git hook installation

### Requirement: Explicit task lists control package installation

When a playbook overrides `git_tasks`, the role SHALL apply only the listed
tasks and SHALL NOT install packages implicitly.

#### Scenario: Explicit list without the package task

- **WHEN** a playbook overrides `git_tasks` and omits `install_packages`
- **THEN** the role does not install packages and relies on the host already
  providing the `git` binary

#### Scenario: Explicit list with the package task

- **WHEN** a playbook overrides `git_tasks` and includes `install_packages`
- **THEN** the role installs packages as part of the selected tasks
