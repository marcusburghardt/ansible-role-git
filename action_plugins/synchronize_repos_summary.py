# SPDX-License-Identifier: Apache-2.0
"""Print a multi-line summary as plain text.

``ansible.builtin.debug`` wraps its message in a JSON result, which turns the
summary's line breaks into ``\n`` escapes. This action prints the text directly
through the display layer and stores it in ``_git_repo_summary`` for tests and
later tasks.
"""

from __future__ import annotations

import re

from ansible.plugins.action import ActionBase
from ansible.utils.display import Display

display = Display()


class ActionModule(ActionBase):
    """Display summary text without the JSON result wrapper."""

    TRANSFERS_FILES = False

    def run(self, tmp=None, task_vars=None):
        """Display the text argument and expose it as a fact."""
        result = super().run(tmp, task_vars)
        text = self._task.args.get("text", "")
        if isinstance(text, list):
            text = "\n".join(str(line) for line in text)
        text = re.sub(r"\n{3,}", "\n\n", str(text).rstrip())
        display.display(text, color="normal")
        result.update(changed=False, ansible_facts={"_git_repo_summary": text})
        return result
