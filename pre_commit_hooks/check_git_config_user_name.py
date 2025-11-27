#!/usr/bin/python
"""This hook checks to ensure the Git config user.name matches one of the specified templates."""

from __future__ import annotations

import argparse
import re
import subprocess
from collections.abc import Sequence


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--templates",
        nargs="+",
        help="One or more templates that the Git config user.name must match.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    argument_parser = build_argument_parser()
    args = argument_parser.parse_args(argv)

    if args.templates:
        proc = subprocess.run(
            ["git", "config", "--get", "user.name"],
            check=False,
            capture_output=True,
            text=True,
        )

        user_name = proc.stdout.strip()

        if not user_name:
            print("Git config user.name is not set.")
            return 1

        for template in args.templates:
            if re.match(template, user_name):
                print(f"Git config user.name is matched to provided template: {template}")
                return 0

        print("Git config user.name is not matched to any provided templates.")
        print(f"Git config user.name: {user_name}")
        print(f"Provided templates: {args.templates}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
