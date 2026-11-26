#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Install the managed commit-msg hook without overwriting foreign hooks."""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

MARKER = "Managed by ansible-role-git"


def run(arguments: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        arguments,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )


def common_directory(repository: Path) -> Path | None:
    result = run(
        [
            "git",
            "-C",
            str(repository),
            "rev-parse",
            "--path-format=absolute",
            "--git-common-dir",
        ]
    )
    if result.returncode != 0:
        result = run(["git", "-C", str(repository), "rev-parse", "--git-common-dir"])
        if result.returncode != 0:
            return None
        value = Path(result.stdout.strip())
        return value if value.is_absolute() else (repository / value).resolve()
    return Path(result.stdout.strip())


def skip(repository: Path, reason: str) -> dict:
    return {"repo": str(repository), "status": "skipped", "reason": reason}


def install(repository: Path, template: Path, on_conflict: str) -> dict:
    repository = repository.expanduser().resolve()
    if not repository.is_dir():
        return skip(repository, "path is not a cloned repository")
    common = common_directory(repository)
    if common is None:
        return skip(repository, "path is not a Git repository")
    hooks_path = run(
        ["git", "-C", str(repository), "config", "--get", "core.hooksPath"]
    )
    if hooks_path.returncode == 0:
        return skip(repository, "core.hooksPath is already configured")

    hook = common / "hooks" / "commit-msg"
    content = template.read_text(encoding="utf-8")
    existed = hook.exists()
    if existed:
        existing = hook.read_text(encoding="utf-8")
        if MARKER not in existing:
            if on_conflict == "fail":
                raise ValueError(f"{repository}: unmanaged commit-msg hook exists")
            return skip(repository, "an unmanaged commit-msg hook already exists")
        if existing == content:
            return {"repo": str(repository), "status": "unchanged"}

    hook.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".commit-msg-", dir=hook.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(content)
        os.chmod(temporary, 0o755)
        os.replace(temporary, hook)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return {"repo": str(repository), "status": "updated" if existed else "installed"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", required=True, help="Rendered hook template")
    parser.add_argument("--repo", action="append", default=[], help="Repository path")
    parser.add_argument(
        "--repos-json", default="[]", help="JSON array of repository paths"
    )
    parser.add_argument("--on-conflict", choices=("skip", "fail"), default="skip")
    arguments = parser.parse_args()
    template = Path(arguments.template)
    if not template.is_file():
        raise ValueError(f"hook template not found: {template}")
    repositories = list(arguments.repo)
    extra = json.loads(arguments.repos_json)
    if not isinstance(extra, list):
        raise ValueError("--repos-json must contain a JSON array")
    repositories.extend(str(repository) for repository in extra)

    results = [
        install(Path(repository), template, arguments.on_conflict)
        for repository in repositories
    ]
    print(
        json.dumps(
            {
                "changed": any(
                    item["status"] in ("installed", "updated") for item in results
                ),
                "results": results,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        print(f"install_commit_hooks: {error}", file=sys.stderr)
        sys.exit(1)
