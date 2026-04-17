## Context

The `ansible-role-git` repository is a published Ansible Galaxy role (`marcusburghardt.git`) with ~20 commits of history. It has no CI/CD pipeline, no automated release process, and is missing standard project hygiene files. The sibling role `ansible-role-ai` has a proven release infrastructure using release-please and GitHub Actions that we will replicate, adapting only where necessary (role name, license, Dependabot ecosystems).

The existing commit history uses free-form messages. Going forward, commits to `main` must follow the Conventional Commits specification for release-please to function.

## Goals / Non-Goals

**Goals:**
- Automate versioning and changelog generation from conventional commits.
- Automate Ansible Galaxy publishing on GitHub Release events.
- Establish consistent YAML linting standards via `.yamllint`.
- Add standard project files (`.gitignore`, `LICENSE`, `CHANGELOG.md`).
- Keep Dependabot watching GitHub Actions dependencies weekly.
- Align license to Apache-2.0 across Ansible roles.

**Non-Goals:**
- Adding Debian/Ubuntu platform support (out of scope for this change).
- Adding pre-commit hooks or a Makefile (future improvement).
- Retroactively reformatting existing commit history.
- Adding CI linting or testing workflows (future improvement).
- Adding SPDX license headers to existing source files.

## Decisions

### 1. Release type: `simple`

**Choice**: Use release-please's `simple` release type (no language-specific version file bumps).

**Rationale**: Ansible roles have no native version file (like `package.json` or `setup.py`). The `simple` type tracks the version solely in `.release-please-manifest.json` and git tags, which is exactly what we need. This matches the AI role's approach.

**Alternatives considered**:
- `node` or `python` release types -- unnecessary since there is no language-specific version to bump.

### 2. Starting version: v1.0.0

**Choice**: Initialize at version 1.0.0.

**Rationale**: The role has been published on Ansible Galaxy and in use. Starting at 0.x would imply instability for a role that is already functional. The v1.0.0 tag also serves as a clean demarcation point: everything before it is pre-automation history, everything after follows conventional commits.

**Alternatives considered**:
- `0.1.0` -- would match the AI role's approach but misrepresents this role's maturity.

### 3. Pre-major bump guards enabled

**Choice**: Set `bump-minor-pre-major: true` and `bump-patch-for-minor-pre-major: true`.

**Rationale**: Consistent with the AI role. These guards are only active while the version is `< 1.0.0`, so they won't affect this role (starting at 1.0.0). Including them ensures consistent configuration if the role were ever reset.

### 4. License: Apache-2.0

**Choice**: Switch from MPL-2.0 to Apache-2.0.

**Rationale**: Aligns with the sibling `ansible-role-ai` role and is a more common license for Ansible Galaxy roles. Apache-2.0 is permissive and well-understood by the community. This is a breaking change that must be clearly communicated.

### 5. Dependabot: github-actions only

**Choice**: Only monitor `github-actions`, skip `pip`.

**Rationale**: The AI role monitors `pip` because it installs Python packages in CI (`ansible-core`). The git role will also install `ansible-core` in the Galaxy publish workflow, but the version is pinned explicitly in the workflow file (`ansible-core==2.17.8`), not managed by pip dependency files. Adding a `pip` ecosystem watch with no requirements file would produce no useful PRs. If a `requirements.txt` is added later, Dependabot can be extended.

**Alternatives considered**:
- Include `pip` for parity -- rejected because there is no pip dependency file to monitor.

### 6. SHA-pinned GitHub Actions

**Choice**: Pin all third-party actions by full SHA with version comments.

**Rationale**: Prevents supply chain attacks from tag mutations. Matches the AI role's practice and aligns with the coding standards' security requirements for GitHub Actions workflows.

### 7. Workflow permissions: principle of least privilege

**Choice**: Set `permissions: {}` at workflow level, grant specific permissions per job.

**Rationale**: Follows the coding standards' requirement that workflows follow the Principle of Least Privilege. The release-please job needs `contents: write` and `pull-requests: write`. The Galaxy publish job needs only `contents: read`.

## Risks / Trade-offs

- **[Breaking license change]** Switching from MPL-2.0 to Apache-2.0 may affect downstream consumers who depend on MPL-2.0 terms. **Mitigation**: Document the change clearly in the CHANGELOG and release notes. The role has a small user base, reducing blast radius.

- **[Conventional commits adoption]** All future commits to `main` must follow conventional commit format or release-please will not generate meaningful changelog entries. **Mitigation**: This is a single-developer repository, so the behavioral change is contained. The commit standards are already documented in the global OpenCode instructions.

- **[GALAXY_API_KEY secret required]** The Galaxy publish workflow requires a `GALAXY_API_KEY` repository secret. If not configured, the workflow will fail silently on the first release. **Mitigation**: Document the secret requirement in the README release process section. Verify the secret exists before the first merge to `main`.

- **[No CI linting gate]** Without a linting workflow, `.yamllint` is advisory only -- it won't block PRs with YAML issues. **Mitigation**: Acceptable for now. Adding a CI linting workflow is a logical follow-up change.

## Open Questions

(None -- all decisions have been made during the explore phase.)
