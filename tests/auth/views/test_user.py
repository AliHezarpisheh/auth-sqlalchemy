"""Unit tests for the UserView class."""

import os
from unittest.mock import patch

import pytest

from auth.views.user import UserView


@pytest.fixture
def user_view() -> UserView:
    """Fixture to instantiate UserView."""
    return UserView()


@pytest.mark.smoke
def test_get_credentials(user_view: UserView) -> None:
    """Test the get_credentials method."""
    with patch("builtins.input") as mock_input, patch(
        "auth.views.user.getpass"
    ) as mock_getpass:
        mock_input.return_value = "test_username"
        mock_getpass.return_value = "test_password"

        username, password = user_view.get_credentials()

    assert username == "test_username"
    assert password == "test_password"

    mock_input.assert_called_once_with("Enter Username: ")
    mock_getpass.assert_called_once_with("Enter Password: ")


@pytest.mark.smoke
def test_show_message(user_view: UserView) -> None:
    """Test the show_message method."""
    msg = "Test Message"
    with patch("builtins.print") as mock_print:
        user_view.show_message(msg)

        mock_print.assert_called_once_with(msg)


def test_clear_screen(user_view: UserView) -> None:
    """Test the clear_screen method."""
    with patch("os.system") as mock_system:
        user_view.clear_screen()

        mock_system.assert_called_once_with("cls" if os.name == "nt" else "clear")
