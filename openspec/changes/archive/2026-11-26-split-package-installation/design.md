# Design

## Context

See `proposal.md` for motivation. The role uses a dispatcher pattern: every
enabled entry in `git_tasks` causes `tasks/main.yml` to include
`vars/<name>.yml` and later `tasks/<name>.yml`. Today `configure_git.yml` holds
both a `become: true` package loop and an unprivileged `ini_file` loop, so the
privileged statement forces `-K` for any run that includes `configure_git`.

All other tasks write only under `ansible_facts['user_dir']`, and only
`synchronize_repos` and `configure_git_hooks` invoke the `git` binary.

## Goals / Non-Goals

**Goals:**

- Make package installation a separate, selectable task.
- Ensure configuration-only runs never attempt privilege escalation.
- Keep the existing dispatcher pattern and OS-specific variable layout.
- Make the breaking change explicit in the release notes.

**Non-Goals:**

- No package-fact pre-check or conditional escalation (decision recorded below).
- No rename of the shared `packages` variable, no split of `redhat.yml`.
- No change to how `git_user_config`, repositories, PS1, scripts, or hooks work.
- No play-level `become` handling; that remains the playbook author's choice.

## Decisions

### New dispatcher task `install_packages`

Add `install_packages` as a `git_tasks` entry, implemented in
`tasks/install_packages.yml`, containing the existing package loop unchanged.
Remove the package block and `become: true` from `tasks/configure_git.yml`.

Rationale: the dispatcher is the role's established control surface; users
already learn it, and `enabled: false` is the obvious way to skip package
management. Alternative considered: a top-level `git_manage_packages` boolean
included outside the dispatcher. Rejected because it introduces a second control
mechanism and diverges from every other task.

### Default ordering: `install_packages` first

Place `install_packages` at the head of the default `git_tasks` list, before
`configure_git` and the tasks that shell out to `git`.

Rationale: `configure_git` only writes an INI file, but `synchronize_repos` and
`configure_git_hooks` require the binary. Default order makes a default run
self-sufficient. Users who reorder the list are responsible for preserving the
dependency; this is documented rather than enforced.

### Keep `packages` in `vars/redhat.yml`

Create `vars/install_packages.yml` with a pointer comment but leave the package
list in the OS-specific file.

Rationale: package names are OS data, and `redhat.yml` is the existing seam if
Debian support is added. Moving the list into the task vars file would tie
package names to the task rather than the platform. Alternative considered:
teaching `main.yml` to skip missing task vars files, which would avoid the
near-empty file but expands the change into dispatcher behavior.

### No conditional escalation in this change

The package task keeps `become: true` and runs whenever enabled; no
`package_facts` gate is added.

Rationale: the immediate requirement is met by disabling the task for
configuration-only runs. A facts gate would avoid the prompt when packages are
already present, but adds a task, a facts dependency, and more logic to a task
meant to stay small. It can be a follow-up change.

### Remove `become` entirely from `configure_git.yml`

The remaining `ini_file` loop needs no escalation.

Rationale: with no privileged statement in the file, omitting
`install_packages` from `git_tasks` guarantees no sudo prompt from the role.

### Accept and document the explicit-list break

Playbooks that override `git_tasks` must add an `install_packages` entry.
Ansible replaces lists, so the role cannot merge in the new default.

Rationale: this is the same consequence the role accepted when
`configure_git_hooks` was added. Documenting it in the README and a
`BREAKING CHANGE:` commit footer is sufficient; a compatibility shim that
implicitly installs packages when the entry is absent would defeat the opt-out
and surprise users.

## Risks / Trade-offs

- **Explicit-list playbooks silently stop installing packages** → document in
  README task selection and examples; add a `BREAKING CHANGE:` footer so
  release-please surfaces it; update the in-repo test playbook's list.
- **Fresh hosts with `install_packages` disabled fail in `git`-dependent
  tasks** → README states the dependency and recommends enabling the task for
  initial provisioning.
- **Play-level `become: true` still prompts** → out of the role's control;
  README example keeps escalation on the task, and the migration plan notes the
  distinction between `-K` and play-level `become`.
- **An almost-empty `vars/install_packages.yml` exists only for the loader** →
  accepted for consistency; noted as a candidate follow-up for the dispatcher.

## Migration Plan

1. Release the change as a breaking feature.
2. For each playbook with an explicit `git_tasks` list, add one entry:
   `{ enabled: true, name: 'install_packages' }` to keep provisioning behavior,
   or `{ enabled: false, name: 'install_packages' }` for configuration-only runs.
3. Fresh hosts need the enabled entry once (with `-K` or passwordless sudo) or
   packages provisioned outside the role.
4. Rollback is a revert of the change; no data migration is involved.
