# Design

## Context

See `proposal.md` - Why. Relevant current state:

- `tasks/synchronize_repos.yml` runs every enabled repository through
  `ansible.builtin.git` with `ignore_errors: true`. `ignore_errors` suppresses
  the stop but not the callback output, so each failure prints the full loop
  item, `Origin`, and module result.
- The remote-management flow is three tasks: a `lineinfile` `state: absent`
  probe in check mode, a `git remote add` command, and an `ini_file` fallback
  gated on `result_git_remote_add is skipped`. That gate is never true for a
  looping task, so the fallback is dead code and a drifted `upstream` URL is
  never corrected.
- `ansible.builtin.git` treats "current branch has no `origin/<branch>`" as a
  hard failure (`reset --hard origin/<branch>`), which is what breaks the
  `REVIEW_MR_*` and topic-branch checkouts.
- The module's dirty check (`has_local_mods`) filters out `??` entries, and
  `force: true` runs `git reset --hard HEAD`, discarding tracked edits with no
  recovery.
- Role support is limited to EL and Fedora; `community.general` is already a
  documented dependency.

## Goals / Non-Goals

**Goals:**

- One output line per repository per task, and no output for disabled entries.
- Preserve local work across updates (stash/restore) and keep current behavior
  safe when restore cannot complete.
- Report every non-updated repository in one grouped, actionable summary.
- Never fail the play; the role is best-effort by decision.
- Cover the changed behavior with a runnable integration playbook.

**Non-Goals:**

- A strict/failing mode or nonzero exit code (explicitly decided against).
- Per-repository `required`, `update`, or `branch` fields.
- Changing authentication, proxy, or credential-helper configuration.
- Reimplementing the `ansible.builtin.git` module or managing submodules.
- Fixing the pre-existing `openspec validate --specs` failure of the repo's
  delta-style main specs.

## Decisions

### Use `failed_when: false` and handle results explicitly

`ignore_errors: true` is the source of the `[ERROR]` blocks. `failed_when:
false` leaves the module's `msg`/`rc`/`stderr` in the registered result but
marks the task successful, so the callback prints a normal one-line result.
Failures are then detected in the summary step (`msg` is defined and `rc` is
nonzero, or `msg` is defined with no `rc`).

Alternative rejected: keeping `ignore_errors` and post-processing the output;
the callback output is emitted before any post-processing and cannot be
suppressed from the role.

### Stash tracked changes instead of forcing

For repositories with tracked changes, run
`git -C <dest> stash push --message "ansible-role-git pre-sync"`, update with
`force: false`, then `git -C <dest> stash pop`. A conflicting pop exits
nonzero and leaves the stash entry in place; the role reports
`[stash-conflict]` with `git stash list` / `git stash pop` recovery commands
and never drops the entry. Check mode skips both stash and pop and reports what
would be stashed.

Untracked files are deliberately excluded from the dirty decision, matching
the module's own `has_local_mods` behavior; `stash -u` would move build output
and other large directories around for no benefit. When `git stash push` reports
that there are no changes to save (the tracked change is confined to a
submodule), the role leaves the repository untouched and reports it under
`dirty` instead of attempting an update that must fail.

Alternatives rejected: `force: true` (irrecoverable loss of tracked edits);
`stash -u` (surprising movement of untracked artifacts); auto-commit (pollutes
history).

### Pre-check state, then update only eligible repositories

A single `git status --porcelain --branch` call per repository supplies the
current branch, its upstream, and tracked-file changes without network access.
The two-character short format keeps path parsing stable, and its `## ` header
carries the branch information that would otherwise need a second call.
Eligibility:

- dirty and `git_repos_dirty_action: skip` -> do not call the update module;
- dirty and `stash` -> stash first;
- dirty and `fail` -> report only;
- no upstream configured -> verify `refs/remotes/origin/<branch>` with
  `git rev-parse --verify --quiet` (second call only for those repositories);
  a missing ref means a local-only review/topic branch, so leave it untouched;
- destination missing -> clone via the normal update path.

Alternative rejected: relying on the module's failure text to classify these
cases, which keeps the destructive `reset --hard` attempt and adds network
round-trips.

### One idempotent remote task

Replace the three tasks with:

```yaml
community.general.git_config:
  name: "remote.{{ item.remote_name }}.url"
  value: "{{ item.remote }}"
  scope: local
  repo: "{{ git_base_dir }}/{{ item.dest }}"
```

It adds a missing remote, corrects a drifted URL, and reports `changed: false`
on repeat runs. Alternatives rejected: `lineinfile` header probing (does not
detect URL drift), `git remote add` (fails when the remote exists), `ini_file`
(no idempotent check, and currently unreachable).

### Summary template plus a signature map

Render `templates/synchronize_repos_summary.j2` through
`lookup('template', ...)` inside one `debug` task. The classification table
(category, regex patterns, remediation text) lives in
`vars/synchronize_repos.yml`, so adding a signature is a data edit, not a task
edit. The template redacts `://user[:token]@` to `://***@` before printing.

Alternatives rejected: a filter plugin (extra machinery and packaging for a
presentation concern) and inline Jinja in the task (unreadable and hard to
test).

### Print the summary through a small action plugin

`ansible.builtin.debug` serialises its message, so the summary's line breaks
become `\n` escapes and the whole report is one hard-to-read JSON string.
`action_plugins/synchronize_repos_summary.py` prints the rendered template
through `Display.display()` and stores it in `_git_repo_summary` for tests.
Alternatives rejected: a `debug` message split into a list (still JSON-wrapped,
quoted per line) and a callback plugin (changes output for every task).

### Buckets and output contract

Results are bucketed as `updated`, `ok`, `skipped`, and `problem`. `skipped`
covers local-only branches and dirty repositories left alone; `problem` covers
auth, network, stash conflicts, and anything unclassified. The summary prints
counts, then one block per problem with name, destination, one-line reason,
and remediation. A clean run prints only the counts line. No `fail` task is
created and no `git_repos_strict` variable is introduced.

## Risks / Trade-offs

- [Stash pop conflicts leave a conflicted tree] -> Keep the stash entry, report
  the conflict with recovery commands, and cover it in the integration
  playbook; the user always retains the original work.
- [A newly created remote branch may look local-only if refs are stale] ->
  Seen only when a local branch shares a name with an unfetched new remote
  branch; the summary names the repository and states that a fetch may be
  needed before the next run.
- [Parsing porcelain output is brittle] -> Only the `## ` branch header and
  the three-character status prefix are read, and the integration playbook
  exercises real `git` output rather than fixtures.
- [`failed_when: false` hides failures from Ansible's recap] -> The summary is
  the single reporting surface, counted in the playbook, and documented in the
  README.
- [Template output is generated in one task] -> If the template raises, the
  play fails at the summary; the integration playbook runs the clean,
  dirty, conflict, and unreachable cases so this is caught early.

## Migration Plan

No data migration. Behavior changes on upgrade: local-only branches are no
longer reset, dirty repositories are stashed instead of reported as failed, and
drifted fork remotes are corrected. Rollback is a revert of the merge; any
stash created by the role is named `ansible-role-git pre-sync` and remains
available via `git stash list`.
