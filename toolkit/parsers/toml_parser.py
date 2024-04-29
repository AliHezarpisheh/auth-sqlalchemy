"""Contains the TOMLParser class for parsing TOML files."""

from typing import Any

import tomlkit

from .base import Parser


class TOMLParser(Parser):
    """Parses TOML files and loads their content."""

    def read_toml(self) -> Any:
        """
        Read a TOML file and return its content as a dictionary.

        Returns
        -------
        Any
            The parsed content of the TOML file.
        """
        try:
            with self._file_path.open(mode="rb") as file:
                content = tomlkit.load(file)
            return content
        except FileNotFoundError:
            print(f"This path is unreachable: `{self._file_path}`!")
        except tomlkit.exceptions.ParseError:
            print(f"Syntax Error in: `{self._file_path}`!")
