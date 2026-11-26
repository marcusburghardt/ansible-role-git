# Spec Delta

## MODIFIED Requirements

### Requirement: Complete feature list

The README SHALL include a bullet list of all features the role provides,
covering all six tasks: install_packages, configure_git, configure_ps,
add_supporting_scripts, synchronize_repos, and configure_git_hooks.

#### Scenario: All tasks represented

- **WHEN** a user reads the feature list
- **THEN** they see entries for independent package installation, user-level Git
  configuration, PS1 prompt customization, supporting script deployment,
  repository synchronization with fork/upstream management, and commit-message
  hook management

### Requirement: Task selection documentation

The README SHALL explain the task dispatcher pattern (`git_tasks`) including how
to enable or disable individual tasks, list all available tasks with their names
and purposes, and identify `install_packages` as the only task requiring
privilege escalation.

#### Scenario: User understands task control

- **WHEN** a user reads the task selection section
- **THEN** they understand how to set `enabled: true/false` for each task in the
  `git_tasks` list to control which features are applied

#### Scenario: User understands the privilege boundary

- **WHEN** a user wants to apply only user-level Git configuration without a
  sudo password
- **THEN** they understand that disabling `install_packages` removes the only
  privileged step from the role

#### Scenario: User is warned about explicit overrides

- **WHEN** a user supplies an explicit `git_tasks` list
- **THEN** they understand that tasks omitted from the list are not applied,
  including package installation

### Requirement: Progressive example playbooks

The README SHALL include at least 4 example playbooks ordered from minimal to
complex, each with a bold label and a fenced YAML code block, and each showing
an explicit `install_packages` entry in its `git_tasks` list.

#### Scenario: Minimal example

- **WHEN** a user wants basic Git configuration
- **THEN** they find an example that enables `configure_git` and `configure_ps`
  with `install_packages` disabled

#### Scenario: Full setup example

- **WHEN** a user wants all features
- **THEN** they find an example enabling all six tasks, including
  `install_packages`, with repository definitions and custom git config

#### Scenario: Fork management example

- **WHEN** a user manages forked repositories
- **THEN** they find an example showing `git_repos` entries with upstream remote
  configuration
