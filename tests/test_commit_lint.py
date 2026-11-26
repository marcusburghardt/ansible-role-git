# SPDX-License-Identifier: Apache-2.0
"""Offline tests for the commit message validator."""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "files/scripts/commit_lint.py"
SPEC = importlib.util.spec_from_file_location("commit_lint", HELPER)
commit_lint = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(commit_lint)


class CommitLintTests(unittest.TestCase):
    def test_valid_commit_message(self) -> None:
        message = (
            "feat(parser): add bounded cache\n"
            "\n"
            "Cache parsed documents up to a fixed size.\n"
            "\n"
            "Signed-off-by: Jane Doe <jane@example.com>\n"
            "Assisted-by: OpenCode (claude-opus-4-6)\n"
        )
        result = commit_lint.validate_commit_message(
            message, require_signed_off_by=True, require_assisted_by=True
        )
        self.assertFalse(result["skipped"])
        self.assertEqual(result["type"], "feat")
        self.assertEqual(result["scope"], "parser")
        self.assertFalse(result["breaking"])

    def test_subject_rules(self) -> None:
        invalid = (
            "Add a cache",
            "feat: add a cache.",
            "feature: add a cache",
            "feat:",
            "feat: " + "x" * 80,
        )
        for subject in invalid:
            with self.subTest(subject=subject):
                with self.assertRaises(ValueError):
                    commit_lint.validate_commit_message(subject)

    def test_breaking_change_marker(self) -> None:
        result = commit_lint.validate_commit_message(
            "feat(api)!: remove legacy endpoint\n\n"
            "BREAKING CHANGE: use /v2 instead.\n\n"
            "Signed-off-by: Jane Doe <jane@example.com>\n",
            require_signed_off_by=True,
        )
        self.assertTrue(result["breaking"])

    def test_body_line_length_and_exemptions(self) -> None:
        long_body = "word " * 16
        with self.assertRaisesRegex(ValueError, "body line 3"):
            commit_lint.validate_commit_message(
                "feat: add cache\n\n"
                f"{long_body}\n\n"
                "Signed-off-by: Jane Doe <jane@example.com>\n"
            )
        result = commit_lint.validate_commit_message(
            "feat: add cache\n\n"
            "See https://example.com/a/very/long/url/that/exceeds/the/limit\n"
            "Signed-off-by: Jane Doe <jane@example.com>\n"
        )
        self.assertFalse(result["skipped"])

    def test_required_trailers(self) -> None:
        with self.assertRaisesRegex(ValueError, "Signed-off-by"):
            commit_lint.validate_commit_message("feat: add cache\n")
        with self.assertRaisesRegex(ValueError, "Assisted-by"):
            commit_lint.validate_commit_message(
                "feat: add cache\n\nSigned-off-by: Jane Doe <jane@example.com>\n",
                require_assisted_by=True,
            )
        with self.assertRaisesRegex(ValueError, "Assisted-by"):
            commit_lint.validate_commit_message(
                "feat: add cache\n\n"
                "Signed-off-by: Jane Doe <jane@example.com>\n"
                "Assisted-by: OpenCode\n",
                require_assisted_by=True,
            )

    def test_exempt_messages(self) -> None:
        for subject in (
            "Merge branch 'main' into feature",
            'Revert "feat: add cache"',
            "fixup! feat: add cache",
            "squash! feat: add cache",
            "amend! feat: add cache",
        ):
            with self.subTest(subject=subject):
                result = commit_lint.validate_commit_message(subject)
                self.assertTrue(result["skipped"])

    def test_cli(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            message = Path(directory) / "COMMIT_EDITMSG"
            message.write_text(
                "docs: explain the commit hook\n\n"
                "Signed-off-by: Jane Doe <jane@example.com>\n",
                encoding="utf-8",
            )
            valid = subprocess.run(
                [
                    sys.executable,
                    str(HELPER),
                    "--file",
                    str(message),
                    "--require-signed-off-by",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(valid.returncode, 0, valid.stderr)
            self.assertFalse(json.loads(valid.stdout)["skipped"])
            message.write_text("Add a cache\n", encoding="utf-8")
            invalid = subprocess.run(
                [sys.executable, str(HELPER), "--file", str(message)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(invalid.returncode, 0)
            self.assertIn("subject", invalid.stderr)


if __name__ == "__main__":
    unittest.main()
