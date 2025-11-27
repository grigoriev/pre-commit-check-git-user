#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="pre-commit-check-git-user",
    description="Pre-commit hooks for checking Git user settings.",
    url="https://github.com/grigoriev/pre-commit-check-git-user",
    version="0.9.1",
    author="Sergey Grigoriev",
    author_email="s.grigoriev@gmail.com",
    packages=["pre_commit_hooks"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "check-git-config-user-email = pre_commit_hooks.check_git_config_user_email:main",
            "check-git-config-user-name = pre_commit_hooks.check_git_config_user_name:main",
        ]
    },
)
