# Changelog

## [2.0.0](https://github.com/marcusburghardt/ansible-role-git/compare/v1.0.1...v2.0.0) (2026-04-17)


### ⚠ BREAKING CHANGES

* License changed from MPL-2.0 to Apache-2.0.

### Features

* add CI/CD release infrastructure and project hygiene files ([acfa398](https://github.com/marcusburghardt/ansible-role-git/commit/acfa3987ecd65fdc7f5589cd659f09168e478734))


### Bug Fixes

* correct exception raising in review_pr.py ([22e8e74](https://github.com/marcusburghardt/ansible-role-git/commit/22e8e748a1c5086a8a5c80e63370f53dce090626))


### Miscellaneous

* archive completed changes and sync specs to main ([82acee1](https://github.com/marcusburghardt/ansible-role-git/commit/82acee1eecdd7895ec04a01ee76d02ce246cc18b))
* **main:** release 1.0.1 ([ba0ff3f](https://github.com/marcusburghardt/ansible-role-git/commit/ba0ff3f55892046ccea4a1ecc8101bbae56ee07f))
* **main:** release 1.0.1 ([6fa9fc6](https://github.com/marcusburghardt/ansible-role-git/commit/6fa9fc6e14efb2be976fe9077b936d43267e3f4c))


### Documentation

* rewrite README with comprehensive role documentation ([176660b](https://github.com/marcusburghardt/ansible-role-git/commit/176660b11b22636c68b98bdf6c495e3350cb1afb))

## [1.0.1](https://github.com/marcusburghardt/ansible-role-git/compare/v1.0.0...v1.0.1) (2026-04-17)


### Bug Fixes

* correct exception raising in review_pr.py ([22e8e74](https://github.com/marcusburghardt/ansible-role-git/commit/22e8e748a1c5086a8a5c80e63370f53dce090626))


### Miscellaneous

* archive completed changes and sync specs to main ([82acee1](https://github.com/marcusburghardt/ansible-role-git/commit/82acee1eecdd7895ec04a01ee76d02ce246cc18b))


### Documentation

* rewrite README with comprehensive role documentation ([176660b](https://github.com/marcusburghardt/ansible-role-git/commit/176660b11b22636c68b98bdf6c495e3350cb1afb))

## [1.0.0](https://github.com/marcusburghardt/ansible-role-git/releases/tag/v1.0.0) (2026-04-17)

### Features

* Install and configure Git with customizable settings
* Configure PS1 prompt to show current git branch and status
* Synchronize and manage multiple git repositories with remote references
* Deploy supporting scripts (review_pr.py) to user bin directory
* Data-driven git configuration via `git_user_config` variable

### Miscellaneous

* Add CI/CD infrastructure with release-please and Galaxy publishing
* Add Dependabot for GitHub Actions dependency updates
* Add `.yamllint` configuration for consistent YAML linting
* Switch license from MPL-2.0 to Apache-2.0
