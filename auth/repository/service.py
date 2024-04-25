"""
Service module for user operations not related to database interactions.

This module contains the UserService class, which provides methods for user-related
operations that are not directly related to database interactions. It serves as a
service layer responsible for handling user registration, password hashing, and
password verification.
"""

from hashlib import sha256
from typing import Optional

from auth.models import User

from .bll import UserBusinessLogicLayer
from .dal import UserDataAccessLayer


class UserService:
    """Service class for user operations."""

    def __init__(self) -> None:
        """Initialize the UserService."""
        self.bll = UserBusinessLogicLayer()
        self.dal = UserDataAccessLayer()

    def register(self, username: str, password: str) -> User:
        """
        Register a new user with the provided username and password.

        Parameters
        ----------
        username : str
            The username of the user.
        password : str
            The password of the user.

        Returns
        -------
        User
            The newly registered User object.
        """
        hashed_password = self.hash_password(password)
        user = self.bll.create_user(username=username, password=hashed_password)
        return user

    def login(self, username: str, password: str) -> tuple[Optional[User], bool]:
        """
        Log in a user with the provided username and password.

        Parameters
        ----------
        username : str
            The username of the user.
        password : str
            The password of the user.

        Returns
        -------
        tuple[Optional[User], bool]
            A tuple containing the User object if authentication is successful,
            otherwise None, and a boolean indicating whether the user is authenticated.
        """
        hashed_password = self.hash_password(password)
        user = self.dal.get_user_by_username(username=username)
        is_authenticated = self.is_authenticated(user, hashed_password)
        return user, is_authenticated

    def is_authenticated(self, user: Optional[User], hashed_password: str) -> bool:
        """
        Check if a user is authenticated based on their password hash.

        Parameters
        ----------
        user : Optional[User]
            The user object to authenticate.
        hashed_password : str
            The hashed password to compare with the user's password hash.

        Returns
        -------
        bool
            True if the user is authenticated, False otherwise.
        """
        if user:
            is_authenticated = user.password == hashed_password
        else:
            is_authenticated = False
        return is_authenticated

    def hash_password(self, password: str) -> str:
        """
        Hash the provided password using SHA-256 algorithm.

        Parameters
        ----------
        password : str
            The password to be hashed.

        Returns
        -------
        str
            The hashed password.
        """
        hashed_password = sha256(password.encode()).hexdigest()
        return hashed_password

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify if the provided password matches the hashed password.

        Parameters
        ----------
        password : str
            The password to be verified.
        hashed_password : str
            The hashed password stored in the database.

        Returns
        -------
        bool
            True if the password matches the hashed password, False otherwise.
        """
        return hashed_password == self.hash_password(password)
