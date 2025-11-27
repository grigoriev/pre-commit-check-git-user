#!/usr/bin/python
"""This hook checks to ensure the Git config user.email matches one of the specified templates."""

from __future__ import annotations

import argparse
import re
import subprocess
from collections.abc import Sequence
from typing import Final

EMAIL_PATTERN: Final[str] = r"^\S+@\S+\.\S+$"


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--templates",
        nargs="+",
        help="One or more templates that the Git config user.email must match.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    argument_parser = build_argument_parser()
    args = argument_parser.parse_args(argv)

    if args.templates:
        proc = subprocess.run(
            ["git", "config", "--get", "user.email"],
            check=False,
            capture_output=True,
            text=True,
        )

        user_email = proc.stdout.strip()

        if not user_email:
            print("Git config user.email is not set.")
            return 1

        if not re.match(EMAIL_PATTERN, user_email):
            print("Git config user.email does not look like an email address.")
            print(f"Git config user.email: {user_email}")
            return 1

        for template in args.templates:
            if re.match(template, user_email):
                print(f"Git config user.email is matched to provided template: {template}")
                return 0

        print("Git config user.email is not matched to any provided templates.")
        print(f"Git config user.email: {user_email}")
        print(f"Provided templates: {args.templates}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
