"""Module for defining base configurations."""

import secrets

from .database.base import DatabaseConnection

db = DatabaseConnection()

PEPPER = secrets.token_urlsafe(40).encode()
