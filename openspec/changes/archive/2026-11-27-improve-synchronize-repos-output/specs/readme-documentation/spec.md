# Spec Delta

## MODIFIED Requirements

### Requirement: Repository synchronization documentation

The README SHALL document the `git_repos` variable structure including all
fields (enabled, name, repo, dest, remote, remote_name), the fork/upstream
management pattern, the `git_repos_dirty_action` and `git_repos_auth_hint`
variables, the grouped synchronization summary, and recovery from a stash
conflict.

#### Scenario: User can configure repos

- **WHEN** a user reads the repository synchronization section
- **THEN** they understand how to define repositories for cloning, how to set
  up upstream remotes for forks, and how to disable remote tracking when not
  needed

#### Scenario: User understands dirty worktree handling

- **WHEN** a user reads the dirty worktree behavior
- **THEN** they understand that `git_repos_dirty_action` controls whether local
  changes are stashed, skipped, or reported

#### Scenario: User can recover from a stash conflict

- **WHEN** the role reports a stash conflict
- **THEN** the README explains that the stash entry is preserved and shows the
  commands to inspect and reapply it

#### Scenario: User understands the summary output

- **WHEN** a user reads the synchronization output documentation
- **THEN** they understand the updated, ok, skipped, and problem buckets, why
  the play stays green, and that review branches are reported but not modified
