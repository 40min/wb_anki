"""Tests for the word parser module."""

from unittest.mock import mock_open, patch

import pytest

from src.wb_anki.parser.parser import parse_word_pairs, read_input


class TestParseWordPairs:
    """Test cases for parse_word_pairs function."""

    def test_parse_valid_word_pairs(self):
        """Test parsing valid word pairs with different delimiters."""
        lines = [
            "hello - world",
            "foo -- bar",
            "test --- example",
            "word\ttranslation",
        ]
        result = parse_word_pairs(lines)

        expected = [
            ("hello", "world"),
            ("foo", "bar"),
            ("test", "example"),
            ("word", "translation"),
        ]
        assert result == expected

    def test_parse_with_whitespace(self):
        """Test parsing with extra whitespace."""
        lines = [
            "  hello  -  world  ",
            "\thello\t--\tworld\t",
        ]
        result = parse_word_pairs(lines)

        expected = [
            ("hello", "world"),
            ("hello", "world"),
        ]
        assert result == expected

    def test_skip_empty_lines(self):
        """Test that empty lines are skipped."""
        lines = [
            "hello - world",
            "",
            "   ",
            "foo - bar",
        ]
        result = parse_word_pairs(lines)

        expected = [
            ("hello", "world"),
            ("foo", "bar"),
        ]
        assert result == expected

    def test_skip_invalid_format(self):
        """Test that invalid lines are skipped."""
        lines = [
            "hello - world",
            "invalid line without delimiter",
            "foo - bar",
            "multiple-dashes-but-no-space",
        ]
        result = parse_word_pairs(lines)

        expected = [
            ("hello", "world"),
            ("foo", "bar"),
        ]
        assert result == expected

    def test_skip_empty_words(self):
        """Test that lines with empty words are skipped."""
        lines = [
            " - world",
            "hello - ",
            "foo - bar",
        ]
        result = parse_word_pairs(lines)

        expected = [("foo", "bar")]
        assert result == expected


class TestReadInput:
    """Test cases for read_input function."""

    @patch("builtins.open", new_callable=mock_open, read_data="hello - world\nfoo - bar")
    def test_read_from_file(self, mock_file):
        """Test reading from a file."""
        result = read_input("test_file.txt")

        expected = ["hello - world\n", "foo - bar"]
        assert result == expected
        mock_file.assert_called_once_with("test_file.txt", "r", encoding="utf-8")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_read_from_nonexistent_file(self, mock_file):
        """Test reading from a non-existent file raises click.Abort."""
        import click

        with pytest.raises(click.Abort):
            read_input("nonexistent.txt")

    @patch("click.get_text_stream")
    def test_read_from_stdin(self, mock_stdin):
        """Test reading from stdin."""
        mock_stdin.return_value.readlines.return_value = ["hello - world\n", "foo - bar\n"]

        result = read_input(None)

        expected = ["hello - world\n", "foo - bar\n"]
        assert result == expected
        mock_stdin.assert_called_once_with("stdin")
