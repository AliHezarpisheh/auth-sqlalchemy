"""Entrypoint for the application, initializing and running the main module."""

from pathlib import Path

from config import setup_logging
from core import Main

LOGGING_CONFIG_PATH = "logging.toml"


if __name__ == "__main__":
    setup_logging(Path(LOGGING_CONFIG_PATH))
    main = Main()
    main.run()
