"""
Service module for user operations not related to database interactions.

This module contains the UserService class, which provides methods for user-related
operations that are not directly related to database interactions. It serves as a
service layer responsible for handling user registration, password hashing, and
password verification.
"""

import hashlib

from auth.models import User
from config.base import PEPPER

from .bll import UserBusinessLogicLayer


class UserService:
    """Service class for user operations."""

    def __init__(self) -> None:
        """Initialize the UserService with a UserBusinessLogicLayer instance."""
        self.bll = UserBusinessLogicLayer()

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

    def hash_password(self, password: str) -> str:
        """
        Hash the provided password using PBKDF2-HMAC algorithm with SHA-256.

        Parameters
        ----------
        password : str
            The password to be hashed.

        Returns
        -------
        str
            The hashed password.
        """
        hashed_password = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), PEPPER, 100_000
        )
        return str(PEPPER + hashed_password)

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
        pepper = hashed_password[: len(PEPPER)]
        stored_hash = hashed_password[len(PEPPER) :]
        computed_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            pepper.encode("utf-8"),
            100_000,
        )
        return stored_hash == str(computed_hash)
