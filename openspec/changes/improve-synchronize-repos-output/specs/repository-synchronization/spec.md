# Spec Delta

## Purpose

Keep the managed Git repositories current with their remotes while leaving
intentional local work intact and reporting only the repositories that need
attention.

## ADDED Requirements

### Requirement: Only enabled repositories are processed

The role SHALL process only repositories whose `enabled` field is true and
SHALL skip disabled repositories without per-repository loop output.

#### Scenario: Disabled repository is not processed

- **WHEN** a `git_repos` entry has `enabled: false`
- **THEN** the role does not clone, fetch, update, or configure that repository
- **AND** no loop output is emitted for it

### Requirement: Update output is one labelled line per repository

For each processed repository, the role SHALL emit at most one line per task
and that line SHALL identify the repository by its `name` rather than printing
the repository data structure.

#### Scenario: Large inventory stays readable

- **WHEN** the role processes dozens of repositories
- **THEN** the update and remote configuration tasks print one line per
  repository
- **AND** the printed line contains the repository name, not the full entry

### Requirement: Dirty worktrees are stashed and restored

When a repository has changes to tracked files and `git_repos_dirty_action` is
`stash`, the role SHALL stash those changes before updating and SHALL restore
them after the update.

#### Scenario: Local edits survive an update

- **WHEN** a repository has uncommitted changes to tracked files
- **AND** `git_repos_dirty_action` is `stash`
- **THEN** the role stashes the changes, updates the repository, and reapplies
  the stash

#### Scenario: Stash conflict preserves local work

- **WHEN** reapplying the stash conflicts with the updated working tree
- **THEN** the role keeps the stash entry instead of dropping it
- **AND** the summary reports the conflict and the commands needed to recover

#### Scenario: Dirty worktree is skipped

- **WHEN** a repository has uncommitted changes and `git_repos_dirty_action` is
  `skip`
- **THEN** the role does not modify that repository
- **AND** the summary reports it as skipped

#### Scenario: Changes that cannot be stashed are reported

- **WHEN** the tracked change is confined to a dirty submodule, which
  `git stash` cannot capture
- **THEN** the role leaves the repository untouched
- **AND** the summary reports it under `dirty` with an explanation instead of
  reporting a stash conflict

### Requirement: Local-only branches are left untouched

When the checked-out branch of a repository has no matching reference under
`origin`, the role SHALL leave the repository unchanged and report it as
informational rather than as a failure.

#### Scenario: Review branch is not reset

- **WHEN** a repository is checked out on a local branch such as `REVIEW_MR_2`
  that has no `origin/REVIEW_MR_2` reference
- **THEN** the role does not reset or switch that repository
- **AND** the summary lists it as an informational skip

### Requirement: Fork remotes are configured idempotently

For every repository with a `remote` URL, the role SHALL ensure the local
remote named by `remote_name` points at that URL, correcting an existing
mismatched URL and reporting no change when it already matches.

#### Scenario: Missing remote is added

- **WHEN** a forked repository has no remote with the configured name
- **THEN** the role creates it with the configured URL

#### Scenario: Mismatched remote URL is corrected

- **WHEN** the existing remote URL differs from the configured `remote`
- **THEN** the role updates the remote URL

#### Scenario: Repeated run reports no change

- **WHEN** the remote already points at the configured URL
- **THEN** the role reports the repository as unchanged

### Requirement: Problems are summarized with remediation

The role SHALL print one grouped summary after synchronization that classifies
each problem as authentication, dirty worktree, network, or other and includes
a remediation hint for the class.

#### Scenario: Authentication failure is actionable

- **WHEN** a remote rejects access with HTTP 403 or an access-denied message
- **THEN** the summary groups the repository under authentication
- **AND** includes the configured remediation hint
- **AND** does not print the raw module error block

#### Scenario: Clean run is quiet

- **WHEN** every repository is already up to date
- **THEN** the summary reports the counts and no problem entries

### Requirement: Synchronization never fails the play

The role SHALL NOT fail the play when repositories cannot be synchronized; it
SHALL record the outcome and continue with remaining tasks.

#### Scenario: Unreachable remote does not abort the play

- **WHEN** a remote is unreachable or a repository cannot be updated
- **THEN** the role continues with the remaining repositories and tasks
- **AND** the play completes successfully
- **AND** the failure appears in the summary

### Requirement: Credentials are redacted from output

The summary SHALL redact embedded credentials from repository URLs before
displaying them.

#### Scenario: Token in URL is masked

- **WHEN** a configured repository URL contains a username or token before the
  host
- **THEN** the summary replaces that user information with a redaction marker
