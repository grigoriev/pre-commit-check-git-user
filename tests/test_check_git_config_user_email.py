"""Tests for check_git_config_user_email hook."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING
from unittest.mock import MagicMock, patch

import pytest

from pre_commit_hooks.check_git_config_user_email import (
    EMAIL_PATTERN,
    build_argument_parser,
    main,
)

if TYPE_CHECKING:
    pass


class TestBuildArgumentParser:
    """Tests for argument parser."""

    def test_parser_with_single_template(self) -> None:
        parser = build_argument_parser()
        args = parser.parse_args(["--templates", ".*@example.com"])
        assert args.templates == [".*@example.com"]

    def test_parser_with_multiple_templates(self) -> None:
        parser = build_argument_parser()
        args = parser.parse_args(["--templates", ".*@company.com", ".*@org.com"])
        assert args.templates == [".*@company.com", ".*@org.com"]

    def test_parser_without_templates(self) -> None:
        parser = build_argument_parser()
        args = parser.parse_args([])
        assert args.templates is None


class TestEmailPattern:
    """Tests for EMAIL_PATTERN constant."""

    @pytest.mark.parametrize(
        "email",
        [
            "user@example.com",
            "john.doe@company.org",
            "test+label@gmail.com",
            "user_name@domain.co.uk",
            "first-last@sub.domain.com",
            "user123@test123.org",
            "a@b.co",
        ],
    )
    def test_valid_emails_match(self, email: str) -> None:
        """Valid email addresses should match the pattern."""
        assert re.match(EMAIL_PATTERN, email), f"Expected {email} to match"

    @pytest.mark.parametrize(
        "email",
        [
            "not-an-email",
            "@example.com",
            "user@",
            "user@domain",
            "user@domain..com",
            "user@@domain.com",
            "user@.domain.com",
            "user@domain.c",
            "",
            "user@ domain.com",
            "user @domain.com",
            "user@domain .com",
        ],
    )
    def test_invalid_emails_do_not_match(self, email: str) -> None:
        """Invalid email addresses should not match the pattern."""
        assert not re.match(EMAIL_PATTERN, email), f"Expected {email} to NOT match"


class TestMain:
    """Tests for main function."""

    def test_no_templates_returns_zero(self) -> None:
        """When no templates provided, should return 0."""
        result = main([])
        assert result == 0

    @patch("pre_commit_hooks.check_git_config_user_email.subprocess.run")
    def test_user_email_not_set(self, mock_run: MagicMock, capsys: pytest.CaptureFixture[str]) -> None:
        """When git user.email is not set, should return 1."""
        mock_run.return_value = MagicMock(stdout="", returncode=1)

        result = main(["--templates", ".*"])
        captured = capsys.readouterr()

        assert result == 1
        assert "Git config user.email is not set" in captured.out

    @patch("pre_commit_hooks.check_git_config_user_email.subprocess.run")
    def test_user_email_matches_template(self, mock_run: MagicMock, capsys: pytest.CaptureFixture[str]) -> None:
        """When git user.email matches template, should return 0."""
        mock_run.return_value = MagicMock(stdout="john@example.com\n", returncode=0)

        result = main(["--templates", ".*@example.com"])
        captured = capsys.readouterr()

        assert result == 0
        assert "matched to provided template" in captured.out

    @patch("pre_commit_hooks.check_git_config_user_email.subprocess.run")
    def test_user_email_matches_one_of_multiple_templates(
        self, mock_run: MagicMock, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """When git user.email matches one of multiple templates, should return 0."""
        mock_run.return_value = MagicMock(stdout="jane@company.org\n", returncode=0)

        result = main(["--templates", ".*@example.com", ".*@company.org"])
        captured = capsys.readouterr()

        assert result == 0
        assert "matched to provided template" in captured.out

    @patch("pre_commit_hooks.check_git_config_user_email.subprocess.run")
    def test_user_email_does_not_match_any_template(
        self, mock_run: MagicMock, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """When git user.email doesn't match any template, should return 1."""
        mock_run.return_value = MagicMock(stdout="bob@other.net\n", returncode=0)

        result = main(["--templates", ".*@example.com", ".*@company.org"])
        captured = capsys.readouterr()

        assert result == 1
        assert "not matched to any provided templates" in captured.out
        assert "bob@other.net" in captured.out

    @patch("pre_commit_hooks.check_git_config_user_email.subprocess.run")
    def test_exact_match_template(self, mock_run: MagicMock) -> None:
        """When template is exact match, should work correctly."""
        mock_run.return_value = MagicMock(stdout="john@example.com\n", returncode=0)

        result = main(["--templates", "^john@example.com$"])

        assert result == 0

    @patch("pre_commit_hooks.check_git_config_user_email.subprocess.run")
    def test_whitespace_stripped(self, mock_run: MagicMock) -> None:
        """Git output whitespace should be stripped."""
        mock_run.return_value = MagicMock(stdout="  john@example.com  \n", returncode=0)

        result = main(["--templates", "john@example.com"])

        assert result == 0

    @patch("pre_commit_hooks.check_git_config_user_email.subprocess.run")
    def test_invalid_email_format_returns_error(self, mock_run: MagicMock, capsys: pytest.CaptureFixture[str]) -> None:
        """When email doesn't look like email, should return 1."""
        mock_run.return_value = MagicMock(stdout="not-an-email\n", returncode=0)

        result = main(["--templates", ".*"])
        captured = capsys.readouterr()

        assert result == 1
        assert "does not look like an email" in captured.out

    @patch("pre_commit_hooks.check_git_config_user_email.subprocess.run")
    def test_consecutive_dots_in_domain_rejected(self, mock_run: MagicMock, capsys: pytest.CaptureFixture[str]) -> None:
        """Email with consecutive dots in domain should be rejected."""
        mock_run.return_value = MagicMock(stdout="user@domain..com\n", returncode=0)

        result = main(["--templates", ".*"])
        captured = capsys.readouterr()

        assert result == 1
        assert "does not look like an email" in captured.out

    @patch("pre_commit_hooks.check_git_config_user_email.subprocess.run")
    def test_email_without_tld_rejected(self, mock_run: MagicMock, capsys: pytest.CaptureFixture[str]) -> None:
        """Email without TLD should be rejected."""
        mock_run.return_value = MagicMock(stdout="user@domain\n", returncode=0)

        result = main(["--templates", ".*"])
        captured = capsys.readouterr()

        assert result == 1
        assert "does not look like an email" in captured.out
