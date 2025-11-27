"""Tests for check_git_config_user_name hook."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import MagicMock, patch

import pytest

from pre_commit_hooks.check_git_config_user_name import build_argument_parser, main

if TYPE_CHECKING:
    pass


class TestBuildArgumentParser:
    """Tests for argument parser."""

    def test_parser_with_single_template(self) -> None:
        parser = build_argument_parser()
        args = parser.parse_args(["--templates", "John Doe"])
        assert args.templates == ["John Doe"]

    def test_parser_with_multiple_templates(self) -> None:
        parser = build_argument_parser()
        args = parser.parse_args(["--templates", "John.*", "Jane.*"])
        assert args.templates == ["John.*", "Jane.*"]

    def test_parser_without_templates(self) -> None:
        parser = build_argument_parser()
        args = parser.parse_args([])
        assert args.templates is None


class TestMain:
    """Tests for main function."""

    def test_no_templates_returns_zero(self) -> None:
        """When no templates provided, should return 0."""
        result = main([])
        assert result == 0

    @patch("pre_commit_hooks.check_git_config_user_name.subprocess.run")
    def test_user_name_not_set(self, mock_run: MagicMock, capsys: pytest.CaptureFixture[str]) -> None:
        """When git user.name is not set, should return 1."""
        mock_run.return_value = MagicMock(stdout="", returncode=1)

        result = main(["--templates", ".*"])
        captured = capsys.readouterr()

        assert result == 1
        assert "Git config user.name is not set" in captured.out

    @patch("pre_commit_hooks.check_git_config_user_name.subprocess.run")
    def test_user_name_matches_template(self, mock_run: MagicMock, capsys: pytest.CaptureFixture[str]) -> None:
        """When git user.name matches template, should return 0."""
        mock_run.return_value = MagicMock(stdout="John Doe\n", returncode=0)

        result = main(["--templates", "John.*"])
        captured = capsys.readouterr()

        assert result == 0
        assert "matched to provided template" in captured.out

    @patch("pre_commit_hooks.check_git_config_user_name.subprocess.run")
    def test_user_name_matches_one_of_multiple_templates(
        self, mock_run: MagicMock, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """When git user.name matches one of multiple templates, should return 0."""
        mock_run.return_value = MagicMock(stdout="Jane Smith\n", returncode=0)

        result = main(["--templates", "John.*", "Jane.*"])
        captured = capsys.readouterr()

        assert result == 0
        assert "matched to provided template" in captured.out

    @patch("pre_commit_hooks.check_git_config_user_name.subprocess.run")
    def test_user_name_does_not_match_any_template(
        self, mock_run: MagicMock, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """When git user.name doesn't match any template, should return 1."""
        mock_run.return_value = MagicMock(stdout="Bob Wilson\n", returncode=0)

        result = main(["--templates", "John.*", "Jane.*"])
        captured = capsys.readouterr()

        assert result == 1
        assert "not matched to any provided templates" in captured.out
        assert "Bob Wilson" in captured.out

    @patch("pre_commit_hooks.check_git_config_user_name.subprocess.run")
    def test_exact_match_template(self, mock_run: MagicMock) -> None:
        """When template is exact match, should work correctly."""
        mock_run.return_value = MagicMock(stdout="John Doe\n", returncode=0)

        result = main(["--templates", "^John Doe$"])

        assert result == 0

    @patch("pre_commit_hooks.check_git_config_user_name.subprocess.run")
    def test_partial_match_at_start(self, mock_run: MagicMock) -> None:
        """re.match only matches at the start of string."""
        mock_run.return_value = MagicMock(stdout="John Doe\n", returncode=0)

        result = main(["--templates", "John"])

        assert result == 0

    @patch("pre_commit_hooks.check_git_config_user_name.subprocess.run")
    def test_whitespace_stripped(self, mock_run: MagicMock) -> None:
        """Git output whitespace should be stripped."""
        mock_run.return_value = MagicMock(stdout="  John Doe  \n", returncode=0)

        result = main(["--templates", "John Doe"])

        assert result == 0

    # Edge cases: Unicode characters
    @patch("pre_commit_hooks.check_git_config_user_name.subprocess.run")
    def test_unicode_name_cyrillic(self, mock_run: MagicMock, capsys: pytest.CaptureFixture[str]) -> None:
        """Should handle Cyrillic characters in names."""
        mock_run.return_value = MagicMock(stdout="Иван Иванов\n", returncode=0)

        result = main(["--templates", "Иван.*"])
        captured = capsys.readouterr()

        assert result == 0
        assert "matched to provided template" in captured.out

    @patch("pre_commit_hooks.check_git_config_user_name.subprocess.run")
    def test_unicode_name_chinese(self, mock_run: MagicMock, capsys: pytest.CaptureFixture[str]) -> None:
        """Should handle Chinese characters in names."""
        mock_run.return_value = MagicMock(stdout="张伟\n", returncode=0)

        result = main(["--templates", "张.*"])
        captured = capsys.readouterr()

        assert result == 0
        assert "matched to provided template" in captured.out

    @patch("pre_commit_hooks.check_git_config_user_name.subprocess.run")
    def test_unicode_name_with_diacritics(self, mock_run: MagicMock, capsys: pytest.CaptureFixture[str]) -> None:
        """Should handle diacritics in names."""
        mock_run.return_value = MagicMock(stdout="José García\n", returncode=0)

        result = main(["--templates", "José.*"])
        captured = capsys.readouterr()

        assert result == 0
        assert "matched to provided template" in captured.out

    # Edge cases: Special characters
    @patch("pre_commit_hooks.check_git_config_user_name.subprocess.run")
    def test_name_with_hyphen(self, mock_run: MagicMock) -> None:
        """Should handle hyphenated names."""
        mock_run.return_value = MagicMock(stdout="Mary-Jane Watson\n", returncode=0)

        result = main(["--templates", "Mary-Jane.*"])

        assert result == 0

    @patch("pre_commit_hooks.check_git_config_user_name.subprocess.run")
    def test_name_with_apostrophe(self, mock_run: MagicMock) -> None:
        """Should handle names with apostrophes."""
        mock_run.return_value = MagicMock(stdout="O'Brien\n", returncode=0)

        result = main(["--templates", "O'Brien"])

        assert result == 0

    @patch("pre_commit_hooks.check_git_config_user_name.subprocess.run")
    def test_name_with_period(self, mock_run: MagicMock) -> None:
        """Should handle names with periods (e.g., initials)."""
        mock_run.return_value = MagicMock(stdout="J. R. R. Tolkien\n", returncode=0)

        # Note: . in regex matches any character, so we escape it
        result = main(["--templates", r"J\. R\. R\. Tolkien"])

        assert result == 0

    @patch("pre_commit_hooks.check_git_config_user_name.subprocess.run")
    def test_single_name(self, mock_run: MagicMock) -> None:
        """Should handle single-word names."""
        mock_run.return_value = MagicMock(stdout="Madonna\n", returncode=0)

        result = main(["--templates", "^Madonna$"])

        assert result == 0

    @patch("pre_commit_hooks.check_git_config_user_name.subprocess.run")
    def test_name_with_numbers(self, mock_run: MagicMock) -> None:
        """Should handle names containing numbers."""
        mock_run.return_value = MagicMock(stdout="John Doe 3rd\n", returncode=0)

        result = main(["--templates", "John Doe.*"])

        assert result == 0

    @patch("pre_commit_hooks.check_git_config_user_name.subprocess.run")
    def test_empty_name_after_strip(self, mock_run: MagicMock, capsys: pytest.CaptureFixture[str]) -> None:
        """Should reject names that are only whitespace."""
        mock_run.return_value = MagicMock(stdout="   \n", returncode=0)

        result = main(["--templates", ".*"])
        captured = capsys.readouterr()

        assert result == 1
        assert "Git config user.name is not set" in captured.out
