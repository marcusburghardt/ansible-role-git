## Context

The README is the primary documentation artifact for an Ansible Galaxy role. Users discover roles on Galaxy, read the README to evaluate fit, and reference it during configuration. The current README was scaffolded and never updated to match the role's actual capabilities. The sibling `ansible-role-ai` role demonstrates a proven documentation pattern with comprehensive variable tables, progressive examples, and feature subsections.

## Goals / Non-Goals

**Goals:**
- Make all role features discoverable and configurable without reading source code.
- Follow the documentation pattern established by `ansible-role-ai` (RST-style headings, variable tables, progressive examples).
- Document all variables, their types, defaults, and purposes.
- Provide example playbooks for common use cases from minimal to fully-featured.
- Accurately document requirements and platform limitations.

**Non-Goals:**
- Changing any role behavior or code (documentation only).
- Adding new features or variables.
- Creating separate documentation files beyond README.md.
- Translating documentation to other languages.

## Decisions

### 1. Follow the ansible-role-ai README structure

**Choice**: Mirror the proven documentation structure from the AI role: RST-style top-level headings, Markdown `###` subsections, variable tables, fenced code blocks for examples, and progressive playbook examples.

**Rationale**: Consistency across roles in the same collection reduces cognitive load for users. The AI role's README has been validated through use and provides a tested template.

### 2. Document all variables in a single Key Variables table

**Choice**: Create one comprehensive table with Variable, Description, and Default columns covering all user-facing variables from `defaults/main.yml`.

**Rationale**: A single table gives users a scannable overview. Subsections can then expand on complex variables (`git_user_config`, `git_repos`) with detailed explanations and examples.

### 3. Progressive example playbooks

**Choice**: Provide 5 example playbooks ordered from minimal to complex: basic git config, full setup, custom gitconfig entries, fork management, and selective task control.

**Rationale**: Users with simple needs can copy the first example. Users with complex setups can find a relevant example that matches their use case. This mirrors the AI role's approach of 8 progressive examples.

### 4. Document community.general as a requirement

**Choice**: Add `community.general` collection to the Requirements section with an install command.

**Rationale**: The role uses `community.general.ini_file` in `configure_git.yml`. Without this collection installed, the role fails. This is a factual requirement that was omitted from the original README.

## Risks / Trade-offs

- **[Documentation drift]** Documentation may become stale as the role evolves. **Mitigation**: The README references `defaults/main.yml` for authoritative defaults, and the release-please workflow encourages documenting changes via conventional commits.
