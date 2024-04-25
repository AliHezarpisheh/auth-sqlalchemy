"""Module defining various enumeration classes used throughout the core commands."""

from enum import StrEnum


class Menu(StrEnum):
    """An enumeration class representing menu options."""

    LOGIN = "L"
    REGISTER = "R"
    QUIT = "Q"
