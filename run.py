"""Entrypoint for the application, initializing and running the main module."""

from config.base import logging_configurator
from core import Main

if __name__ == "__main__":
    logging_configurator.setup()
    main = Main()
    main.run()
