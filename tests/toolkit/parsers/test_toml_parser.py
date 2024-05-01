"""Unit tests for the TOMLParser class."""

from unittest.mock import mock_open, patch

import pytest

from toolkit.parsers.toml_parser import TOMLParser

SAMPLE_TOML_CONTENT = """
[info]
name = "John"
age = 30
"""

FILE_PATH = "test.toml"


@pytest.fixture
def toml_parser() -> TOMLParser:
    """Fixture to instantiate TOMLParser."""
    return TOMLParser(file_path=FILE_PATH)


@pytest.mark.smoke
def test_read(toml_parser: TOMLParser) -> None:
    """Test reading a valid TOML file."""
    with patch("pathlib.Path.open", mock_open(read_data=SAMPLE_TOML_CONTENT)):
        content = toml_parser.read()

    assert content == {"info": {"name": "John", "age": 30}}


def test_read_not_found_toml_file(
    toml_parser: TOMLParser, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test reading a non-existing file."""
    with patch("pathlib.Path.open") as mock_open:
        mock_open.side_effect = FileNotFoundError
        toml_parser.read()

    assert capsys.readouterr().out == "This path is unreachable: `test.toml`!\n"


def test_read_invalid_syntax_toml_file(
    toml_parser: TOMLParser, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test reading an invalid TOML file."""
    with patch("pathlib.Path.open", mock_open(read_data="invalid syntax")):
        toml_parser.read()

    assert capsys.readouterr().out == "Syntax Error in: `test.toml`!\n"
