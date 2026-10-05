#!/usr/bin/python3

"""
This script creates a local branch with the code from an Upstream PR or MR.
It is useful for Upstream maintainers who quite often need to download the code
to review and test proposed changes in a local environment.

It supports both GitHub (PRs) and GitLab (MRs) by auto-detecting the forge
from the remote URL. Use --forge to override when auto-detection is not
sufficient (e.g. self-hosted instances with custom domains).

It must be called from the repository to which the PR/MR belongs.

Author: Marcus Burghardt <maburgha@redhat.com>
"""

import argparse
import subprocess
import sys

FORGE_GITHUB = "github"
FORGE_GITLAB = "gitlab"
SUPPORTED_FORGES = [FORGE_GITHUB, FORGE_GITLAB]

REF_FORMATS = {
    FORGE_GITHUB: "pull/{number}/head:{branch}",
    FORGE_GITLAB: "merge-requests/{number}/head:{branch}",
}

BRANCH_PREFIXES = {
    FORGE_GITHUB: "REVIEW_PR",
    FORGE_GITLAB: "REVIEW_MR",
}


def detect_forge_type(remote: str) -> str:
    """Detect whether the remote points to GitHub or GitLab."""
    result = subprocess.run(
        ["git", "remote", "get-url", remote],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(
            f"Warning: could not determine URL for remote '{remote}'. "
            f"Defaulting to {FORGE_GITHUB}. Use --forge to override.",
            file=sys.stderr,
        )
        return FORGE_GITHUB

    url = result.stdout.strip().lower()
    if "gitlab" in url:
        return FORGE_GITLAB
    return FORGE_GITHUB


def build_ref(forge: str, number: str, branch: str) -> str:
    """Return the fetch refspec for the given forge type."""
    return REF_FORMATS[forge].format(number=number, branch=branch)


def fetch_pr(remote: str, ref: str):
    return subprocess.run(["git", "fetch", remote, ref])


def update_pr(remote: str, ref: str):
    return subprocess.run(
        ["git", "pull", remote, ref, "--rebase", "--force"]
    )


def checkout_branch(branch_name: str):
    subprocess.run(["git", "checkout", branch_name])


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            "Script to optimize the PR/MR review process in a local "
            "environment. It must be called from the repository to which "
            "the PR/MR belongs. Supports GitHub and GitLab."
        ),
        epilog="Usage example: review_pr.py 12090",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("pr", help="Upstream PR/MR number")
    parser.add_argument(
        "--remote",
        default="upstream",
        help="Remote name linked to the Upstream repository",
    )
    parser.add_argument(
        "--main-branch",
        default="main",
        help="Main branch name in Upstream repository",
    )
    parser.add_argument(
        "--no-checkout",
        action="store_true",
        help="Do not checkout the just created branch",
    )
    parser.add_argument(
        "--forge",
        choices=SUPPORTED_FORGES,
        default=None,
        help=(
            "Force the forge type instead of auto-detecting from the "
            "remote URL. Useful for self-hosted instances."
        ),
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    remote = args.remote
    number = args.pr

    forge = args.forge if args.forge else detect_forge_type(remote)
    prefix = BRANCH_PREFIXES[forge]
    review_branch = f"{prefix}_{number}"
    ref = build_ref(forge, number, review_branch)

    print(f"Detected forge: {forge}")
    fetch_cmd = fetch_pr(remote, ref)

    if fetch_cmd.returncode != 0:
        print(
            f"PR/MR {number} was likely already fetched. "
            "Checking if it is updated."
        )
        update_cmd = update_pr(remote, ref)

        if update_cmd.returncode != 0:
            raise RuntimeError(
                "Failed to fetch or update the PR/MR. "
                "Check the error messages."
            )

    if not args.no_checkout:
        checkout_branch(review_branch)


if __name__ == "__main__":
    main()
