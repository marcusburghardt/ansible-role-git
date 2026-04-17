## 1. Project Hygiene Files

- [x] 1.1 Create root `.gitignore` (OpenSpec/OpenCode framework artifacts, agent tool directories)
- [x] 1.2 Create `.yamllint` configuration (extend default, line-length 200 warning, truthy restricted, ignore `.opencode/` and `openspec/`)
- [x] 1.3 Create `LICENSE` file with Apache License 2.0 full text
- [x] 1.4 Update `meta/main.yml` license field from `MPL` to `Apache-2.0`
- [x] 1.5 Update `README.md` license section to reference Apache-2.0

## 2. Release-Please Configuration

- [x] 2.1 Create `.release-please-manifest.json` with initial version `1.0.0`
- [x] 2.2 Create `release-please-config.json` (simple release type, changelog sections, no component in tag, pre-major bump guards)
- [x] 2.3 Create initial `CHANGELOG.md` for v1.0.0

## 3. GitHub Actions Workflows

- [x] 3.1 Create `.github/workflows/ci_release.yml` (release-please action, SHA-pinned, push to main trigger, least-privilege permissions)
- [x] 3.2 Create `.github/workflows/ci_galaxy_publish.yml` (Galaxy import on release published, SHA-pinned actions, Python 3.12, pinned ansible-core)

## 4. Dependabot Configuration

- [x] 4.1 Create `.github/dependabot.yml` (github-actions ecosystem, weekly schedule, chore prefix with scope)

## 5. Verification

- [x] 5.1 Run `yamllint .` against the repository to verify no YAML issues with existing files
- [x] 5.2 Verify all new files are properly tracked by git (not ignored by `.gitignore`)
