"""Module for controlling user authentication operations."""

from typing import Optional

from ..helpers.exceptions import UserAlreadyExistsError
from ..models import User
from ..repository import UserService
from ..views import UserView


class UserController:
    """Controller class for managing user authentication operations."""

    def __init__(self) -> None:
        """Initialize UserController."""
        self.view = UserView()
        self.service = UserService()

    def register(self) -> Optional[User]:
        """
        Register a new user.

        Returns
        -------
        Optional[User]
            The registered user if successful, otherwise None.
        """
        username, password = self.view.get_credentials()
        try:
            user = self.service.register(username=username, password=password)
        except UserAlreadyExistsError:
            self.view.clear_screen()
            self.view.show_message(
                "\033[91m"  # Red color
                + f"User {username} already exists. Please login instead. "
                + "\033[0m"  # Red color
                + "\U0001f914"  # 🤔
                + "\n"  # Extra blank line
            )
            user = None
        else:
            self.view.clear_screen()
            self.view.show_message(
                "\033[92m"  # Green color
                + f"User {username} is registered successfully. "
                + "\U0001f389"  # 🎉
                + "\033[0m"  # Green color
                + "\n"  # Extra blank line
            )
        return user

    def login(self) -> tuple[Optional[User], bool]:
        """
        Log in an existing user.

        Returns
        -------
        tuple[Optional[User], bool]
            A tuple containing the user object and a boolean indicating
            whether the login attempt was successful.
        """
        username, password = self.view.get_credentials()
        user, is_authenticated = self.service.login(
            username=username, password=password
        )
        self._show_login_msg(user, is_authenticated)
        return user, is_authenticated

    def show_welcome_msg(self) -> None:
        """Display a welcome message to the user."""
        self.view.clear_screen()
        self.view.show_message(
            "\033[94m"  # Blue color
            + "Welcome to the Authentication App!"
            + "\033[0m"  # Blue color
            + "\n"  # Extra blank line
        )

    def _show_login_msg(self, user: Optional[User], is_authenticated: bool) -> None:
        """
        Show a login message based on authentication status.

        Parameters
        ----------
        user : Optional[User]
            The user object if authentication was successful, otherwise None.
        is_authenticated : bool
            A boolean indicating whether the login attempt was successful.
        """
        if is_authenticated and user:
            self.view.clear_screen()
            self.view.show_message(
                "\033[92m"  # Green color
                + f"User {user.username} is logged in successfully. "
                + "\U0001f389"  # 🎉
                + "\033[0m"  # Green color
                + "\n"  # Extra blank line
            )
        else:
            self.view.clear_screen()
            self.view.show_message(
                "\033[91m"  # Red color
                + "Invalid credentials. Please try again. "
                + "\U0001f501"  # 🔁
                + "\033[0m"  # Red color
                + "\n"  # Extra blank line
            )
