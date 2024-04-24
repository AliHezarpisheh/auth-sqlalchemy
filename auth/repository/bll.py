"""
Business Logic Layer for user operations.

This module contains the Business Logic Layer (BLL) responsible for handling
user-related operations, such as creating new users in the database. The BLL acts as an
intermediary between the application's user interface and the data access layer,
encapsulating the business rules and logic governing user management.

The UserBusinessLogicLayer class provides methods for interacting with user data,
ensuring data integrity and enforcing business rules during user creation. It utilizes
SQLAlchemy for database interaction and integrates with the application's user model.
"""

from sqlalchemy.exc import IntegrityError

from auth.models import User
from config.base import db

from ..helpers.exceptions import UserAlreadyExistsError


class UserBusinessLogicLayer:
    """Business Logic Layer for user operations."""

    def create_user(self, username: str, password: str) -> User:
        """
        Create a new user in the database.

        Parameters
        ----------
        username : str
            The username of the user.
        password : str
            The password of the user.

        Returns
        -------
        User
            The newly created User object.

        Raises
        ------
        UserAlreadyExistsError
            If the username already exists in the database.
        """
        user = User(username=username, password=password)
        session = db.get_session()
        with session.begin():
            try:
                session.add(user)
                session.commit()
            except IntegrityError as err:
                session.rollback()
                raise UserAlreadyExistsError(
                    f"User {username} Already Registered."
                ) from err
        return user
