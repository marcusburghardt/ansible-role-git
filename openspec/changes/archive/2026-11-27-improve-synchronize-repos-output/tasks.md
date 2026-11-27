# Tasks

## 1. Variables and constants

- [x] 1.1 Add `git_repos_dirty_action: stash`,
      `git_repos_auth_hint`, and `git_repos_summary_max_file_samples: 5` to
      `defaults/main.yml` with comments explaining the allowed values; verify
      the file parses with `python3 -c "import yaml,sys;
      yaml.safe_load(open('defaults/main.yml'))"`.
- [x] 1.2 Add the error signature map (category, regex patterns, remediation)
      and summary constants to `vars/synchronize_repos.yml`; verify every
      category has at least one pattern and a hint, and that the default auth
      hint includes a placeholder-safe remediation.

## 2. Repository state collection

- [x] 2.1 Derive `_git_repos_enabled` from `git_repos | selectattr('enabled')`
      and replace every loop over `git_repos` with it; verify a run with a
      disabled entry emits no output for that entry.
- [x] 2.2 Add a pre-check loop running
      `git -C <dest> status --porcelain=v2 --branch` with
      `failed_when: false`, `changed_when: false`, and
      `loop_control.label: "{{ item.name }}"`; verify against a fixture with
      tracked changes and one with no repository that both results are
      captured and no task fails.
- [x] 2.3 Add a follow-up check of `refs/remotes/origin/<branch>` for
      repositories whose branch has no configured upstream, treating a missing
      ref as a local-only branch; verify a `REVIEW_MR_*`-style fixture is
      classified as local-only and is not updated.

## 3. Update with stash and restore

- [x] 3.1 Replace the update task body with `force: false`,
      `failed_when: false`, and a `loop_control.label`; verify a run against a
      repository whose remote returns 403 prints no `[ERROR]` or `Origin`
      block.
- [x] 3.2 Add the stash task for tracked changes when
      `git_repos_dirty_action == 'stash'` and the check-mode guard; verify a
      dirty fixture is left clean before the update and that
      `git stash list` shows the named entry during the run.
- [x] 3.3 Add the restore task running `git stash pop`, capturing a nonzero
      result as `stash-conflict` without dropping the entry; verify a
      conflicting fixture keeps exactly one stash entry and preserves the
      conflicted working tree.
- [x] 3.4 Ensure repositories selected by the `skip`/`fail` dirty actions are
      excluded from the update loop and recorded in the result set; verify
      each action leaves the fixture's tracked files untouched.

## 4. Fork remote configuration

- [x] 4.1 Replace the `lineinfile` probe, `git remote add`, and `ini_file`
      tasks with a single `community.general.git_config` task
      (`remote.<name>.url`, `scope: local`, `repo:` the destination) with a
      `loop_control.label`; verify adding a missing remote, correcting a
      drifted URL, and a repeat run that reports no change.
- [x] 4.2 Confirm no reference remains to `result_git_remote_check` or
      `result_git_remote_add` and that the dead `ini_file` fallback is gone;
      verify with `grep -n 'result_git_remote' tasks/synchronize_repos.yml`.

## 5. Summary output and documentation

- [x] 5.1 Add `templates/synchronize_repos_summary.j2` rendering the counts
      line plus one grouped block per problem, using the signature map and
      redacting `://user[:token]@` to `://***@`; verify a fixture run with one
      auth failure prints the auth bucket, the remediation hint, and a redacted
      URL.
- [x] 5.2 Replace the terminal result handling with one `debug` task that
      renders the template via `lookup('template', ...)` and prints nothing but
      the counts line on a clean run; verify no `fail` task and no
      `git_repos_strict` reference exist in the role.
- [x] 5.3 Update the README repository synchronization section and variable
      table with `git_repos_dirty_action`, `git_repos_auth_hint`, the summary
      buckets, and stash-conflict recovery; verify every new default appears in
      the table and the recovery commands are copy-pasteable.

## 6. Integration test playbook

- [x] 6.1 Add `tests/test_synchronize_repos.yml` scaffolding with temporary
      bare remotes and clones under a temp directory, running the role with
      only `synchronize_repos` enabled; verify the playbook runs to completion.
- [x] 6.2 Cover a clean update and re-run, asserting an `ok`/`updated` bucket
      and `changed: false` on the second pass.
- [x] 6.3 Cover a dirty worktree, asserting the edits are restored after the
      update and the repository is not reported as a problem.
- [x] 6.4 Cover a stash conflict, asserting one stash entry remains and the
      summary reports `stash-conflict` with recovery commands.
- [x] 6.5 Cover a local-only review branch, asserting the branch and working
      tree are unchanged and the entry is reported as an informational skip.
- [x] 6.6 Cover an unreachable remote, asserting the play succeeds, the
      repository appears under `problem`, and the raw module error block is
      absent from the output.
- [x] 6.7 Cover upstream URL drift, asserting the configured URL is restored
      and a repeat run reports no change.
- [x] 6.8 Cover an all-clean run, asserting the summary prints counts only,
      with no problem blocks.

## 7. Integration verification

- [x] 7.1 Run `yamllint defaults/main.yml vars/synchronize_repos.yml
      tasks/synchronize_repos.yml tests/test_synchronize_repos.yml` and verify
      it reports no errors.
- [x] 7.2 Run
      `ansible-playbook -i localhost, -c local tests/test_synchronize_repos.yml`
      and verify every assertion passes.
- [x] 7.3 Run `ansible-playbook -i localhost, -c local --syntax-check
      tests/test.yml` and verify the role still parses.
- [x] 7.4 Run `openspec validate improve-synchronize-repos-output --strict` and
      verify the change validates.

## Workflow follow-up

- Archive the change after the project's review requirements are satisfied.
