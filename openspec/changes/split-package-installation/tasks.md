# Tasks

## 1. Split the task

- [x] 1.1 Create `tasks/install_packages.yml` with the existing package loop from
      `configure_git.yml`, keeping `become: true` and the current task label
      format; verify the file parses with `ansible-playbook --syntax-check`.
- [x] 1.2 Create `vars/install_packages.yml` with a comment pointing at the
      OS-specific `packages` list in `vars/redhat.yml`; verify
      `ansible-inventory`/role loading does not report a missing vars file.
- [x] 1.3 Remove the package task and `become: true` from
      `tasks/configure_git.yml`, leaving only the `ini_file` loop; verify with
      `grep -n 'become\|package' tasks/configure_git.yml` that neither remains.
- [x] 1.4 Add `{ enabled: true, name: 'install_packages' }` as the first entry
      in `defaults/main.yml` `git_tasks`; verify the order with
      `yq '.git_tasks' defaults/main.yml` or an equivalent read.
- [x] 1.5 Add `{ enabled: false, name: 'install_packages' }` to the explicit
      `git_tasks` list in `tests/test_git_hooks.yml`; verify the list still has
      every task name present exactly once.

## 2. Documentation and release note

- [x] 2.1 Update the README feature bullet list and the stale task count to
      include `install_packages` (six tasks total); verify no "all 4 tasks" text
      remains with `grep -n '4 tasks' README.md`.
- [x] 2.2 Update the README task selection table and snippet to list
      `install_packages` first and state it is the only task requiring privilege
      escalation; verify the table matches `defaults/main.yml`.
- [x] 2.3 Update every README example `git_tasks` list to include an explicit
      `install_packages` entry, disabled in the minimal example; verify the YAML
      blocks remain valid and internally consistent.
- [x] 2.4 Commit with a Conventional Commit subject plus a `BREAKING CHANGE:`
      footer explaining that explicit `git_tasks` playbooks must add
      `install_packages`; verify with `git log -1 --format=%B`.

## 3. Integration verification

- [x] 3.1 Run the hook test playbook with
      `ansible-playbook -i localhost, -c local tests/test_git_hooks.yml` and
      verify all assertions pass with `install_packages` disabled.
- [x] 3.2 Run a configuration-only play on a host where Git is already installed
      without `-K` and verify no privilege-escalation prompt appears.
- [x] 3.3 Run the role with the default `git_tasks` on a host missing a package
      and verify only `install_packages` requests escalation and package
      installation succeeds.
- [x] 3.4 Run `openspec validate split-package-installation --strict` and verify
      the change validates.

## Workflow follow-up

- Archive the change after review and merge.
