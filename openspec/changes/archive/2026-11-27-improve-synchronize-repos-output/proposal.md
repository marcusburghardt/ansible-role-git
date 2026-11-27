# Proposal

## Why

A single synchronization run over ~50 repositories currently produces thousands
of lines of output: every loop iteration dumps the full repository dictionary,
every expected failure prints a 12-line `[ERROR]` block with duplicated JSON, and
three remote-management tasks leak registered `invocation`/`module_args` data.
The eight failures in the last run (4 × HTTP 403, 2 × review branch with no
`origin` counterpart, 2 × dirty worktree) are real, but the report neither
groups them nor says what to do, so they are hard to act on and easy to ignore.

## What Changes

- Reduce per-repository output to a single labelled line by adding
  `loop_control.label` and filtering disabled repositories out of every loop.
- Stop expected failures from printing `[ERROR]` blocks: replace
  `ignore_errors: true` with `failed_when: false` and handle results explicitly.
- Replace the three-task remote-management chain (`lineinfile` check-mode probe,
  `git remote add`, dead `ini_file` fallback) with one idempotent
  `community.general.git_config` task. This also fixes stale `upstream` URLs,
  which the current probe never corrects.
- Handle dirty worktrees automatically: `git stash push` before the update and
  `git stash pop` after it. A conflicting pop keeps the stash entry and is
  reported with recovery commands. `force: true` is never used, so tracked edits
  cannot be silently discarded.
- Leave repositories on a local branch that has no `origin/<branch>` reference
  untouched and report them as informational; this removes the
  `Failed to checkout branch REVIEW_MR_2` class of failures.
- Emit one grouped summary (new Jinja template) that buckets results into
  `updated`, `ok`, `skipped`, and `problem`, classifies problems by signature
  (auth, dirty, network, other) and prints a copy-pasteable fix per bucket.
- Keep the play green: as decided, the role reports but never fails the play.
- New variables: `git_repos_dirty_action` (`stash` default), `git_repos_auth_hint`,
  and `git_repos_summary_max_file_samples`.

## Capabilities

### New Capabilities

- `repository-synchronization`: behavior of the `synchronize_repos` task —
  quiet idempotent updates, dirty-worktree stash/restore, review-branch
  handling, fork remote configuration, and the grouped diagnostic summary.

### Modified Capabilities

- `readme-documentation`: document the new synchronization variables, the stash
  behavior and its conflict recovery, and the summary output contract.

## Impact

- `tasks/synchronize_repos.yml` — rewritten task flow.
- `vars/synchronize_repos.yml` — error signature and summary constants.
- `templates/synchronize_repos_summary.j2` — new summary template.
- `defaults/main.yml` — three new variables.
- `README.md` — repository synchronization and variable documentation.
- `tests/test_synchronize_repos.yml` — new integration playbook covering clean,
  dirty, conflicting, review-branch, and unreachable repositories.
- No API or dependency changes; `community.general` is already required.
