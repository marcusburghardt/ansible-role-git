## ADDED Requirements

### Requirement: README title and introduction
The README SHALL use the role name `marcusburghardt.git` as the title with RST-style underline formatting. The introduction SHALL describe the role's purpose and reference `defaults/main.yml` for customization.

#### Scenario: Title matches role name
- **WHEN** the README is viewed
- **THEN** the title reads "marcusburghardt.git" with an RST-style `=====` underline

#### Scenario: Introduction explains purpose
- **WHEN** a user reads the introduction
- **THEN** they understand the role installs and configures Git, customizes the shell prompt, manages repositories, and deploys supporting scripts

### Requirement: Complete feature list
The README SHALL include a bullet list of all features the role provides, covering all 4 tasks: configure_git, configure_ps, add_supporting_scripts, and synchronize_repos.

#### Scenario: All tasks represented
- **WHEN** a user reads the feature list
- **THEN** they see entries for Git installation and configuration, PS1 prompt customization, supporting script deployment, and repository synchronization with fork/upstream management

### Requirement: Accurate requirements section
The README SHALL document all prerequisites including Python 3, the `community.general` Ansible collection, and the target platform limitations (EL and Fedora).

#### Scenario: Collection dependency documented
- **WHEN** a user reads the requirements
- **THEN** they find `community.general` listed with the install command `ansible-galaxy collection install community.general`

#### Scenario: Platform limitations documented
- **WHEN** a user reads the requirements
- **THEN** they understand the role currently supports Red Hat Enterprise Linux and Fedora only

### Requirement: Key variables table
The README SHALL include a Markdown table listing all user-facing variables from `defaults/main.yml` with columns for Variable, Description, and Default value.

#### Scenario: All defaults documented
- **WHEN** a user views the variable table
- **THEN** every variable defined in `defaults/main.yml` appears with its default value and a description of its purpose

### Requirement: Task selection documentation
The README SHALL explain the task dispatcher pattern (`git_tasks`) including how to enable or disable individual tasks, and list all available tasks with their names and purposes.

#### Scenario: User understands task control
- **WHEN** a user reads the task selection section
- **THEN** they understand how to set `enabled: true/false` for each task in the `git_tasks` list to control which features are applied

### Requirement: Git configuration documentation
The README SHALL explain the data-driven `git_user_config` variable, including the structure of each entry (enabled, state, section, parameter, value) and how to add custom gitconfig entries.

#### Scenario: User can add custom config
- **WHEN** a user reads the git configuration section
- **THEN** they understand how to add new entries to `git_user_config` to configure arbitrary `~/.gitconfig` sections and parameters

### Requirement: Repository synchronization documentation
The README SHALL document the `git_repos` variable structure including all fields (enabled, name, repo, dest, remote, remote_name) and explain the fork/upstream management pattern.

#### Scenario: User can configure repos
- **WHEN** a user reads the repository synchronization section
- **THEN** they understand how to define repositories for cloning, how to set up upstream remotes for forks, and how to disable remote tracking when not needed

### Requirement: Supporting scripts documentation
The README SHALL document the `add_supporting_scripts` task, the `review_pr.py` script's purpose and usage, and the `git_scripts_dir` variable.

#### Scenario: User understands review_pr.py
- **WHEN** a user reads the supporting scripts section
- **THEN** they understand the script creates a local review branch from an upstream PR and know its CLI arguments

### Requirement: Progressive example playbooks
The README SHALL include at least 4 example playbooks ordered from minimal to complex, each with a bold label and a fenced YAML code block.

#### Scenario: Minimal example
- **WHEN** a user wants basic Git configuration
- **THEN** they find an example that only enables `configure_git` and `configure_ps`

#### Scenario: Full setup example
- **WHEN** a user wants all features
- **THEN** they find an example enabling all 4 tasks with repository definitions and custom git config

#### Scenario: Fork management example
- **WHEN** a user manages forked repositories
- **THEN** they find an example showing `git_repos` entries with upstream remote configuration

### Requirement: Commit standards section
The README SHALL include a section documenting the Conventional Commits requirement for contributions.

#### Scenario: Contributor understands commit format
- **WHEN** a contributor reads the commit standards section
- **THEN** they understand commits must follow the Conventional Commits specification and see the common types (feat, fix, docs, chore, refactor)
