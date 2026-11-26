# Proposal

## Why

The `configure_git` task mixes privileged package installation with unprivileged
user configuration. Because one statement in the file uses `become: true`,
running the role for user-level settings alone still requires a sudo password
(`-K` / `--ask-become-pass`). Users who only want `~/.gitconfig` managed should
not need root access.

## What Changes

- Move the `ansible.builtin.package` loop out of `configure_git.yml` into a new
  `install_packages` task that is the only part of the role requiring privilege
  escalation.
- Remove `become: true` from `configure_git.yml`; it keeps only the
  `community.general.ini_file` loop for `~/.gitconfig`.
- Add `install_packages` as the first entry in the default `git_tasks` list and
  add the supporting `tasks/install_packages.yml` and
  `vars/install_packages.yml` files. The OS-specific `packages` list stays in
  `vars/redhat.yml`.
- **BREAKING**: Playbooks that override `git_tasks` with an explicit list must
  add an `install_packages` entry, otherwise packages are no longer installed.
  Existing hosts that already have Git work unchanged; fresh hosts need the
  entry (or separate provisioning) before tasks that invoke the `git` binary.
- Update README task selection, feature list, examples, and task counts to
  reflect the new task and the privilege boundary.
- Update the Git hook test playbook's explicit `git_tasks` list to include the
  new task as disabled.

## Capabilities

### New Capabilities

- `package-installation`: Defines package installation as an independent,
  opt-out task and establishes that only package installation escalates
  privileges, so user configuration runs without sudo.

### Modified Capabilities

- `readme-documentation`: The feature list, task selection documentation,
  examples, and task counts must include `install_packages` and describe the
  privilege boundary.

## Impact

- `tasks/configure_git.yml` (package block removed, `become` removed)
- `tasks/install_packages.yml` (new)
- `vars/install_packages.yml` (new)
- `defaults/main.yml` (`git_tasks` order and entries)
- `tests/test_git_hooks.yml` (explicit `git_tasks` list)
- `README.md` (task table, examples, feature bullets, task count)
- `openspec/specs/readme-documentation/spec.md` (via delta)
- Release note: breaking change for playbooks with explicit `git_tasks` lists,
  including `dev_rh.yml`-style development playbooks.
