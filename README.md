Role Name
=========

This Ansible Role will ensure the GIT tool is installed and configured according to the user
preferences. Settings can be customized through variables. Take a look in the existing
standards defined in "defaults/main.yml" and overridden them in a Playbook.

This role will:
- Ensure GIT is installed;
- Ensure the proper settings in ~/.gitconfig;
- Ensure the PS1 variable is defined to show the current branch when working in a GIT repository;

To install this role:  
```$ ansible-galaxy role install marcusburghardt.git```

Requirements
------------

- python3

Role Variables
--------------

You can customize your environment in a very simple and centralized way editing some variables in:
- defaults/main.yml

In some rare cases, you may change some configuration to reflect your local environment in:
- vars/*.yml

Observe that the above variables could be set in your Playbook too, which, IMO is much more elegant. ;)
Take a look in the Example Playbook section.

Dependencies
------------

None.

Example Playbook
----------------

This playbook will prepare everything with the right variables.  
For this example, lets call this Playbook file as "ansible_git.yml":

```
---
- hosts: linux
  vars:
    - git_tasks:
      - { enabled: true,  name: 'configure_git' }
      - { enabled: true,  name: 'configure_ps' }
  roles:
    - marcusburghardt.git
```

Considering the inventory file is in the same folder and is called "hosts_git",
you can now run this command:  
```$ ansible-playbook -K -i hosts_git ansible_git.yml```

License
-------

Licensed under the Apache License, Version 2.0.
See the [LICENSE](LICENSE) file for details.

Release Process
---------------

This project uses [release-please](https://github.com/googleapis/release-please)
for automated versioning and changelog generation. Commits to `main` must follow
the [Conventional Commits](https://www.conventionalcommits.org/) specification.

When a release PR is merged, a GitHub Release is created automatically, which
triggers publishing to Ansible Galaxy.

**Note:** The `GALAXY_API_KEY` repository secret must be configured for Galaxy
publishing to work.

Author Information
------------------

Marcus Burghardt
- [https://buymeacoffee.com/marcusburghardt](https://buymeacoffee.com/marcusburghardt)
- [https://github.com/marcusburghardt](https://github.com/marcusburghardt)
- [https://www.linkedin.com/in/marcusburghardt](https://www.linkedin.com/in/marcusburghardt)
