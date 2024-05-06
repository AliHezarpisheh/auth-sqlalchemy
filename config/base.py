"""Module for defining base configurations."""

from toolkit.parsers import TOMLParser

from .database.base import DatabaseConnection
from .logging.base import LoggingConfigurator

# Database
db = DatabaseConnection()

# Logging
LOGGING_CONFIG_PATH = "logging.toml"
toml_parser = TOMLParser(LOGGING_CONFIG_PATH)
logging_configurator = LoggingConfigurator(parser=toml_parser)
