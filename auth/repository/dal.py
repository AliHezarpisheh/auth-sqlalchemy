"""
Data Access Layer for user operations.

This module contains the Data Access Layer (DAL) responsible for handling user-related
operations at the database level. The DAL acts as an intermediary between the
application's business logic layer and the database, encapsulating database queries and
interactions related to user data.

The `UserDataAccessLayer` class provides methods for querying and manipulating user data
in the database. It utilizes SQLAlchemy for database interaction and integrates with the
application's user model to ensure consistency and data integrity.
"""

import logging
from typing import Optional

from config.base import db

from ..models import User

logger = logging.getLogger(__name__)


class UserDataAccessLayer:
    """Data Access Layer for user operations."""

    def __init__(self) -> None:
        """Initialize the UserDataAccessLayer."""
        self.session = db.get_session()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by their username.

        Parameters
        ----------
        username : str
            The username of the user to retrieve.

        Returns
        -------
        Optional[User]
            The user object if found, otherwise ``None``.
        """
        logger.info(f"Retrieving user by username: {username}")

        user: Optional[User] = (
            self.session.query(User).filter_by(username=username).scalar()
        )
        return user
