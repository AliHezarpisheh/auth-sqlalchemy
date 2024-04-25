"""Module for handling user views and interactions."""

import os
from getpass import getpass


class UserView:
    """View class for managing user interface interactions."""

    def get_credentials(self) -> tuple[str, str]:
        """
        Prompt the user to enter their username and password.

        Returns
        -------
        tuple[str, str]
            A tuple containing the entered username and password.
        """
        username = input("Enter Username: ")
        password = getpass("Enter Password: ")
        return username, password

    def show_message(self, msg: str) -> None:
        """
        Display a message to the user.

        Parameters
        ----------
        msg : str
            The message to display.
        """
        print(msg)

    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")
