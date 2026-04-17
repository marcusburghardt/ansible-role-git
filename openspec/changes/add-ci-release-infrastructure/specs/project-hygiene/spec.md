## ADDED Requirements

### Requirement: Root .gitignore
The repository SHALL have a root `.gitignore` file that ignores OpenSpec/OpenCode framework infrastructure, OpenCode plugin artifacts, and agent tool directories (`.cursor`, `.claude`, `CLAUDE.md`).

#### Scenario: Framework artifacts ignored
- **WHEN** `git status` is run in a repository with OpenSpec/OpenCode framework files
- **THEN** framework infrastructure files (`.specify/`, `.opencode/node_modules/`, `.opencode/package.json`, etc.) do not appear as untracked

#### Scenario: Agent directories ignored
- **WHEN** agent tools create `.cursor/`, `.claude/`, or `CLAUDE.md` files
- **THEN** these files do not appear as untracked in `git status`

### Requirement: YAML lint configuration
The repository SHALL have a `.yamllint` configuration file at the root. It SHALL extend the `default` ruleset with: line length warning at 200 characters, truthy values restricted to `true`/`false`, comments requiring a starting space with minimum 1 space from content, braces with max 1 space inside, and implicit octal values forbidden. It SHALL ignore `.opencode/` and `openspec/` directories.

#### Scenario: Yamllint validates role files
- **WHEN** `yamllint .` is run at the repository root
- **THEN** all YAML files in `defaults/`, `vars/`, `tasks/`, `meta/`, `handlers/`, and `tests/` are validated against the configured rules

#### Scenario: Framework directories excluded
- **WHEN** `yamllint .` is run at the repository root
- **THEN** files under `.opencode/` and `openspec/` are not validated

### Requirement: LICENSE file
The repository SHALL contain a `LICENSE` file at the root with the full Apache License 2.0 text. The license in `meta/main.yml` SHALL be updated to `Apache-2.0`. The license section in `README.md` SHALL be updated to reference Apache-2.0.

#### Scenario: License file present
- **WHEN** the repository root is inspected
- **THEN** a `LICENSE` file exists containing the Apache License Version 2.0 full text

#### Scenario: Meta and README consistency
- **WHEN** `meta/main.yml` and `README.md` are read
- **THEN** both reference Apache-2.0 as the license

### Requirement: Initial CHANGELOG
The repository SHALL contain a `CHANGELOG.md` file at the root. The initial content SHALL document the v1.0.0 release. Subsequent releases SHALL be managed automatically by release-please.

#### Scenario: Changelog exists at initial release
- **WHEN** the v1.0.0 release is created
- **THEN** `CHANGELOG.md` exists with an entry for v1.0.0
