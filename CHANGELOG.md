# Changelog

## [3.0.1](https://github.com/marcusburghardt/ansible-role-git/compare/v3.0.0...v3.0.1) (2026-11-27)


### Bug Fixes

* **ci:** publish to Galaxy in release workflow ([0602282](https://github.com/marcusburghardt/ansible-role-git/commit/0602282a7232b216cc82446e065f7925318001d1))

## [3.0.0](https://github.com/marcusburghardt/ansible-role-git/compare/v2.1.0...v3.0.0) (2026-11-27)


### ⚠ BREAKING CHANGES

* Playbooks that override git_tasks with an explicit list must add an install_packages entry, otherwise packages are no longer installed.

### Features

* **hooks:** add opt-in commit-msg validation ([2b75169](https://github.com/marcusburghardt/ansible-role-git/commit/2b7516927aaa2ced8ff58db35e219214aee43c3d))
* split package installation into its own task ([f68ad32](https://github.com/marcusburghardt/ansible-role-git/commit/f68ad32a6c2e4860badde2416ff9b6e06c01140f))
* **sync:** add repository synchronization variables ([b234be1](https://github.com/marcusburghardt/ansible-role-git/commit/b234be16c54890ed528743764a94679cf82ee74a))
* **sync:** rewrite repository update flow with grouped summary ([cf1069c](https://github.com/marcusburghardt/ansible-role-git/commit/cf1069c433706a3b0fb935f26e2f0631ced041fe))


### Miscellaneous

* **deps:** bump actions/checkout from 7.0.0 to 7.0.1 ([54440b2](https://github.com/marcusburghardt/ansible-role-git/commit/54440b2d2ca1ff114e5786ab43889a308e799be6))
* **deps:** bump actions/checkout from 7.0.0 to 7.0.1 ([8e01029](https://github.com/marcusburghardt/ansible-role-git/commit/8e010291153eceec779bbc99b4d34e22bc67a8de))
* **deps:** bump actions/setup-python from 6.3.0 to 7.1.0 ([c96bfaa](https://github.com/marcusburghardt/ansible-role-git/commit/c96bfaa2698ab3a124304f4fc5555ebd00d0df03))
* **deps:** bump actions/setup-python from 6.3.0 to 7.1.0 ([6b8bb4a](https://github.com/marcusburghardt/ansible-role-git/commit/6b8bb4ac23ec9abddf61845dc7748451f523d134))
* ignore Python bytecode caches ([4e3de67](https://github.com/marcusburghardt/ansible-role-git/commit/4e3de674b8e7039cb8048f64cd6d532b739dd4ce))
* **openspec:** archive improve-synchronize-repos-output ([dddede1](https://github.com/marcusburghardt/ansible-role-git/commit/dddede10cc543dcc9d0a980741a92f368f72e3bc))
* **openspec:** archive split-package-installation ([45e8fa6](https://github.com/marcusburghardt/ansible-role-git/commit/45e8fa6eeace8799a92eaadcfbb27231b5f5ed0a))
* **openspec:** mark split package installation tasks complete ([84b6737](https://github.com/marcusburghardt/ansible-role-git/commit/84b67372f17c6bb9d5fb0c5ffe14cf8d818ab436))
* **openspec:** mark synchronize repos tasks complete ([21ab342](https://github.com/marcusburghardt/ansible-role-git/commit/21ab342a8823f1fec99f942ab36f5e7ea87e44d4))
* **openspec:** repair main spec structure ([09e1f09](https://github.com/marcusburghardt/ansible-role-git/commit/09e1f09acd52f0aa7a1dfaa520228d61be524835))


### Documentation

* describe commit-msg hook management ([22a7d5e](https://github.com/marcusburghardt/ansible-role-git/commit/22a7d5e4b04ba2e25973f4bf4b7e9cdece60a9fd))
* **openspec:** propose split package installation ([21a4dcc](https://github.com/marcusburghardt/ansible-role-git/commit/21a4dcc0537021adce87d7e1995932b34d84ea11))
* **openspec:** propose synchronize repos output changes ([20165a0](https://github.com/marcusburghardt/ansible-role-git/commit/20165a045c370126124f1e979012e843e5c0b526))
* **sync:** document update and summary behavior ([1ac6ecd](https://github.com/marcusburghardt/ansible-role-git/commit/1ac6ecd39677738f63ed6b59668b72d422effbce))


### Refactoring

* **hooks:** install hooks in one task ([85320de](https://github.com/marcusburghardt/ansible-role-git/commit/85320de23737c57303f7c7c4b60e46808b0568bd))

## [2.1.0](https://github.com/marcusburghardt/ansible-role-git/compare/v2.0.0...v2.1.0) (2026-10-05)


### Features

* add GitLab CLI (glab) support ([38876a9](https://github.com/marcusburghardt/ansible-role-git/commit/38876a910fec5e7eca57a7f186e6ff422e560815))
* add GitLab merge request support to review_pr.py ([782d14c](https://github.com/marcusburghardt/ansible-role-git/commit/782d14c670f93a80414e77f866af0edf17cca3c4))


### Miscellaneous

* **deps:** bump actions/checkout from 6.0.2 to 7.0.0 ([760e680](https://github.com/marcusburghardt/ansible-role-git/commit/760e68074d1ff84a82ec4f56704ccd20c00e76ef))
* **deps:** bump actions/checkout from 6.0.2 to 7.0.0 ([08e3d17](https://github.com/marcusburghardt/ansible-role-git/commit/08e3d175c560296a986ef505a46c0c9533ef8e7d))
* **deps:** bump actions/setup-python from 6.2.0 to 6.3.0 ([bda0781](https://github.com/marcusburghardt/ansible-role-git/commit/bda0781ac3c5106e098ceb121a37f3cbba781ade))
* **deps:** bump actions/setup-python from 6.2.0 to 6.3.0 ([5916d6b](https://github.com/marcusburghardt/ansible-role-git/commit/5916d6b4371d6bad642c674d79e1cc645246298c))
* **deps:** bump googleapis/release-please-action from 4.4.1 to 5.0.0 ([18f7cc1](https://github.com/marcusburghardt/ansible-role-git/commit/18f7cc1610413fce6b29122b4f36f09035dd349b))
* **deps:** bump googleapis/release-please-action from 4.4.1 to 5.0.0 ([32f48b2](https://github.com/marcusburghardt/ansible-role-git/commit/32f48b214e5f74cf6aa7776ec074c34319d97b38))

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
