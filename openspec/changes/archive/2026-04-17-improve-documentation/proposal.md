## Why

The README was generated from the Ansible Galaxy scaffold and has not been updated to reflect the role's full capabilities. It documents 3 of the 4 tasks, has no variable table, incomplete requirements, and only one minimal example playbook. Users must read source code to understand how to use the role, which violates the principle of self-documenting projects. The sibling `ansible-role-ai` has a comprehensive README (574 lines) that serves as a proven template for documentation quality.

## What Changes

- Rewrite README.md with proper role name title (replace "Role Name" placeholder).
- Add complete feature list covering all 4 tasks (configure_git, configure_ps, add_supporting_scripts, synchronize_repos).
- Add comprehensive variable table documenting all defaults with descriptions and default values.
- Document the task dispatcher pattern (`git_tasks`) so users understand how to selectively enable/disable features.
- Document the data-driven git configuration (`git_user_config`) with examples of adding custom entries.
- Document the repository synchronization feature including fork/upstream management.
- Document the supporting scripts feature and the `review_pr.py` script usage.
- Update requirements to include `community.general` collection dependency.
- Document platform support limitations (EL/Fedora only).
- Add multiple example playbooks covering progressively complex use cases.
- Add a commit standards section.

## Capabilities

### New Capabilities

- `readme-documentation`: Comprehensive README structure covering all role features, variables, examples, and requirements.

### Modified Capabilities

(No existing specs to modify -- the `openspec/specs/` directory only contains specs from the `add-ci-release-infrastructure` change.)

## Impact

- **README.md**: Full rewrite. No code changes, no behavioral changes.
- **User experience**: Users can understand and configure the role without reading source code.
