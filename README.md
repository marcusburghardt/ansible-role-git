marcusburghardt.git
===================

This Ansible role installs and configures Git on Red Hat Enterprise Linux and
Fedora systems. Settings are customizable through variables defined in
`defaults/main.yml` or overridden in your playbook.

This role will:
- Install Git and GitHub CLI (`gh`);
- Configure user-level Git settings in `~/.gitconfig` via a data-driven variable;
- Customize the PS1 prompt to show the current Git branch and working tree status;
- Deploy supporting scripts for PR review workflows;
- Clone, update, and manage Git repositories with fork/upstream remote tracking;
- Deploy a Git hints reference file to the base working directory.

To install this role:
```
ansible-galaxy role install marcusburghardt.git
```

Requirements
------------

- Python 3
- `community.general` Ansible collection (used by `community.general.ini_file`)

```
ansible-galaxy collection install community.general
```

> **Platform support:** This role currently supports Red Hat Enterprise Linux (EL)
> and Fedora only. There are no Debian/Ubuntu variables defined.

Role Variables
--------------

### Key Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `git_tasks` | List of tasks to run (see [Task Selection](#task-selection)) | All 4 tasks enabled |
| `git_base_dir` | Base directory for all Git repositories | `~/GIT` |
| `git_scripts_dir` | Directory for supporting scripts | `~/bin` |
| `git_username` | Git user name for commits | `'Name Surname'` |
| `git_email` | Git email for commits | `'myemail@mydomain.com'` |
| `git_editor` | Default Git editor | `'vim'` |
| `git_autocrlf` | Line ending conversion setting | `'input'` |
| `git_user_config` | Data-driven list of gitconfig entries (see [Git Configuration](#git-configuration)) | 6 default entries |
| `git_repos` | List of repositories to clone and manage (see [Repository Synchronization](#repository-synchronization)) | 2 disabled examples |

### Task Selection

The role uses a task dispatcher pattern. Each task can be individually enabled or
disabled via the `git_tasks` variable:

```yaml
git_tasks:
  - { enabled: true, name: 'configure_git' }
  - { enabled: true, name: 'configure_ps' }
  - { enabled: true, name: 'add_supporting_scripts' }
  - { enabled: true, name: 'synchronize_repos' }
```

| Task | Purpose |
|------|---------|
| `configure_git` | Install Git packages and apply `~/.gitconfig` settings |
| `configure_ps` | Customize PS1 prompt to show branch name and status |
| `add_supporting_scripts` | Deploy helper scripts (e.g., `review_pr.py`) to `git_scripts_dir` |
| `synchronize_repos` | Clone/update repositories, configure fork remotes, deploy hints file |

Set `enabled: false` on any task to skip it.

### Git Configuration

The `git_user_config` variable provides data-driven control over `~/.gitconfig`.
Each entry maps to a section, parameter, and value in the config file:

```yaml
git_user_config:
  - { enabled: true, state: 'present', section: 'core', parameter: 'editor', value: 'vim' }
  - { enabled: true, state: 'present', section: 'core', parameter: 'autocrlf', value: 'input' }
  - { enabled: true, state: 'present', section: 'fetch', parameter: 'pruneTags', value: 'true' }
  - { enabled: true, state: 'present', section: 'http', parameter: 'sslVersion', value: 'tlsv1.3' }
  - { enabled: true, state: 'present', section: 'user', parameter: 'name', value: '{{ git_username }}' }
  - { enabled: true, state: 'present', section: 'user', parameter: 'email', value: '{{ git_email }}' }
```

Each entry has the following fields:

| Field | Description |
|-------|-------------|
| `enabled` | Whether to apply this setting (`true`/`false`) |
| `state` | `present` to set the value, `absent` to remove it |
| `section` | The gitconfig section (e.g., `core`, `user`, `http`) |
| `parameter` | The parameter name within the section |
| `value` | The value to set |

To add custom entries, append to the list in your playbook. For example, to
enable GPG signing:

```yaml
git_user_config:
  - { enabled: true, state: 'present', section: 'commit', parameter: 'gpgSign', value: 'true' }
  - { enabled: true, state: 'present', section: 'user', parameter: 'signingKey', value: 'ABCDEF1234567890' }
```

### Repository Synchronization

The `git_repos` variable defines repositories to clone, update, and optionally
configure with upstream remotes for fork workflows:

```yaml
git_repos:
  - { enabled: true, name: 'MyFork->Upstream',
      repo: 'https://github.com/myuser/project.git',
      dest: 'Project/repository',
      remote: 'https://github.com/upstream-org/project.git',
      remote_name: 'upstream' }

  - { enabled: true, name: 'DirectClone',
      repo: 'https://github.com/someorg/tool.git',
      dest: 'Tools/tool',
      remote: false,
      remote_name: 'upstream' }
```

Each entry has the following fields:

| Field | Description |
|-------|-------------|
| `enabled` | Whether to process this repository (`true`/`false`) |
| `name` | Descriptive label for the repository |
| `repo` | Git URL to clone from (your fork or the main repo) |
| `dest` | Destination path relative to `git_base_dir` |
| `remote` | URL for the upstream remote, or `false` to skip remote setup |
| `remote_name` | Name for the upstream remote (typically `upstream`) |

Repositories are cloned into `git_base_dir/<dest>`. When `remote` is set to a URL,
the role configures an additional remote so you can fetch upstream changes with
`git fetch upstream`.

The task also deploys a `GIT_HINTS.md` reference file to `git_base_dir` with
tips on authentication, branching, rebasing, and troubleshooting.

### Supporting Scripts

When `add_supporting_scripts` is enabled, the role deploys helper scripts to
`git_scripts_dir` (default: `~/bin`).

**`review_pr.py`** -- Creates a local branch from an upstream PR for code review:

```
review_pr.py <pr_number> [--remote upstream] [--main-branch main] [--no-checkout]
```

| Argument | Description | Default |
|----------|-------------|---------|
| `pr_number` | PR number to fetch (positional, required) | -- |
| `--remote` | Remote name linked to the upstream repository | `upstream` |
| `--main-branch` | Main branch name in the upstream repository | `main` |
| `--no-checkout` | Do not checkout the review branch after fetching | -- |

The script creates a branch named `REVIEW_PR_<number>` and checks it out.
If the PR was already fetched, it updates the branch via rebase.

Dependencies
------------

None.

Example Playbook
----------------

**Minimal -- Git config and prompt only:**

```yaml
---
- hosts: linux
  vars:
    git_username: 'Jane Doe'
    git_email: 'jane@example.com'
    git_tasks:
      - { enabled: true, name: 'configure_git' }
      - { enabled: true, name: 'configure_ps' }
      - { enabled: false, name: 'add_supporting_scripts' }
      - { enabled: false, name: 'synchronize_repos' }
  roles:
    - marcusburghardt.git
```

**Full setup with repository synchronization:**

```yaml
---
- hosts: linux
  vars:
    git_username: 'Jane Doe'
    git_email: 'jane@example.com'
    git_base_dir: "{{ ansible_facts['user_dir'] }}/Projects"
    git_repos:
      - { enabled: true, name: 'MyFork->Upstream',
          repo: 'https://github.com/janedoe/cool-project.git',
          dest: 'CoolProject/cool-project',
          remote: 'https://github.com/cool-org/cool-project.git',
          remote_name: 'upstream' }
      - { enabled: true, name: 'TeamRepo',
          repo: 'https://github.com/my-team/shared-tools.git',
          dest: 'Team/shared-tools',
          remote: false,
          remote_name: 'upstream' }
  roles:
    - marcusburghardt.git
```

**Custom gitconfig entries (GPG signing, pull rebase):**

```yaml
---
- hosts: linux
  vars:
    git_username: 'Jane Doe'
    git_email: 'jane@example.com'
    git_user_config:
      - { enabled: true, state: 'present', section: 'core', parameter: 'editor', value: 'vim' }
      - { enabled: true, state: 'present', section: 'core', parameter: 'autocrlf', value: 'input' }
      - { enabled: true, state: 'present', section: 'fetch', parameter: 'pruneTags', value: 'true' }
      - { enabled: true, state: 'present', section: 'http', parameter: 'sslVersion', value: 'tlsv1.3' }
      - { enabled: true, state: 'present', section: 'user', parameter: 'name', value: '{{ git_username }}' }
      - { enabled: true, state: 'present', section: 'user', parameter: 'email', value: '{{ git_email }}' }
      - { enabled: true, state: 'present', section: 'commit', parameter: 'gpgSign', value: 'true' }
      - { enabled: true, state: 'present', section: 'pull', parameter: 'rebase', value: 'true' }
    git_tasks:
      - { enabled: true, name: 'configure_git' }
      - { enabled: false, name: 'configure_ps' }
      - { enabled: false, name: 'add_supporting_scripts' }
      - { enabled: false, name: 'synchronize_repos' }
  roles:
    - marcusburghardt.git
```

**Selective tasks -- only synchronize repositories:**

```yaml
---
- hosts: linux
  vars:
    git_base_dir: "{{ ansible_facts['user_dir'] }}/GIT"
    git_repos:
      - { enabled: true, name: 'Ansible-Role-Git',
          repo: 'https://github.com/marcusburghardt/ansible-role-git.git',
          dest: 'AnsibleRoles/ansible-role-git',
          remote: false,
          remote_name: 'upstream' }
    git_tasks:
      - { enabled: false, name: 'configure_git' }
      - { enabled: false, name: 'configure_ps' }
      - { enabled: false, name: 'add_supporting_scripts' }
      - { enabled: true, name: 'synchronize_repos' }
  roles:
    - marcusburghardt.git
```

Commit Standards
----------------

This project follows the [Conventional Commits](https://www.conventionalcommits.org/)
specification. All commits to `main` must use the format:

```
<type>[optional scope]: <description>
```

Common types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`.

Release Process
---------------

This project uses [release-please](https://github.com/googleapis/release-please)
for automated versioning and changelog generation. Commits to `main` must follow
the [Conventional Commits](https://www.conventionalcommits.org/) specification.

When a release PR is merged, a GitHub Release is created automatically, which
triggers publishing to Ansible Galaxy.

**Note:** The `GALAXY_API_KEY` repository secret must be configured for Galaxy
publishing to work.

License
-------

Apache-2.0

Author Information
------------------

Marcus Burghardt
- [https://buymeacoffee.com/marcusburghardt](https://buymeacoffee.com/marcusburghardt)
- [https://github.com/marcusburghardt](https://github.com/marcusburghardt)
- [https://www.linkedin.com/in/marcusburghardt](https://www.linkedin.com/in/marcusburghardt)
