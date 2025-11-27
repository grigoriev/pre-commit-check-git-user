#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This hook checks to ensure the Git config user.email matches one of the specified templates."""

import argparse
import re
import subprocess

EMAIL_PATTERN = r"^\S+@\S+\.\S+$"


def build_argument_parser():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--templates",
        nargs="+",
        help="One or more templates that the Git config user.email must match.",
    )
    return parser


def main(argv=None):
    argument_parser = build_argument_parser()
    args = argument_parser.parse_args(argv)

    retval = 0
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
        elif re.match(EMAIL_PATTERN, user_email):
            print("Git config user.email does not look like an email address.")
            print("Git config user.email: " + user_email)
            return 1
        else:
            for template in args.templates:
                if re.match(template, user_email):
                    print(
                        "Git config user.email is matched to provided template: "
                        + template
                    )
                    return 0
            print("Git config user.email is not matched to any provided templates.")
            print("Git config user.email: " + user_email)
            print("Provided templates: " + str(args.templates))
            return 1


if __name__ == "__main__":
    exit(main())
