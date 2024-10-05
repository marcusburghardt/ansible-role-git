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

---
- hosts: linux
  vars:
    - git_tasks:
      - { enabled: true,  name: 'configure_git' }
      - { enabled: true,  name: 'configure_ps' }
  roles:
    - marcusburghardt.git

Considering the inventory file is in the same folder and is called "hosts_git",
you can now run this command:  
```$ ansible-playbook -K -i hosts_git ansible_git.yml```

License
-------

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

Author Information
------------------

Marcus Burghardt
- https://buymeacoffee.com/marcusburghardt
- https://github.com/marcusburghardt/
- https://www.linkedin.com/in/marcusburghardt/
