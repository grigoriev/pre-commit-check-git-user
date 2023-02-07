#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This hook checks to ensure the Git config user.name matches one of the specified templates."""

import argparse
import re
import subprocess


def build_argument_parser():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--templates",
        nargs="+",
        help="One or more templates that the Git config user.name must match.",
    )
    return parser


def main(argv=None):
    argument_parser = build_argument_parser()
    args = argument_parser.parse_args(argv)

    retval = 0
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
        else:
            for template in args.templates:
                if re.match(template, user_name):
                    print("Git config user.name is matched to provided template: " + template)
                    return 0
            print("Git config user.name is not matched to any provided templates.")
            print("Git config user.name: " + user_name)
            print("Provided templates: " + str(args.templates))
            return 1


if __name__ == "__main__":
    exit(main())
