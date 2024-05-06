"""Unit tests for the UserController class."""

from typing import Generator
from unittest.mock import MagicMock, patch

import pytest

from auth.controllers.user import UserController
from auth.helpers.exceptions import UserAlreadyExistsError


@pytest.fixture(autouse=True)
def mock_service() -> Generator[MagicMock, None, None]:
    """Fixture for mocking the UserService."""
    with patch("auth.controllers.user.UserService") as mock_service:
        yield mock_service


@pytest.fixture(autouse=True)
def mock_view() -> Generator[MagicMock, None, None]:
    """Fixture for mocking the UserView."""
    with patch("auth.controllers.user.UserView") as mock_view:
        yield mock_view


@pytest.fixture
def user_controller() -> UserController:
    """Fixture for instantiating a UserController."""
    return UserController()


def test_register_success(
    user_controller: UserController, mock_service: MagicMock, mock_view: MagicMock
) -> None:
    """Test case for successful user registration."""
    mock_view.return_value.get_credentials.return_value = (
        "test_username",
        "test_password",
    )

    user_controller.register()

    mock_service.return_value.register.assert_called_once_with(
        username="test_username", password="test_password"
    )
    mock_view.return_value.clear_screen.assert_called_once()
    mock_view.return_value.show_message.assert_called_once()


def test_register_failure(
    user_controller: UserController, mock_service: MagicMock, mock_view: MagicMock
) -> None:
    """Test case for user registration failure."""
    mock_view.return_value.get_credentials.return_value = (
        "test_username",
        "test_password",
    )
    mock_service.return_value.register.side_effect = UserAlreadyExistsError

    user_controller.register()

    mock_service.return_value.register.assert_called_once_with(
        username="test_username", password="test_password"
    )
    mock_view.return_value.clear_screen.assert_called_once()
    mock_view.return_value.show_message.assert_called_once()


def test_login_success(
    user_controller: UserController, mock_service: MagicMock, mock_view: MagicMock
) -> None:
    """Test case for successful user login."""
    mock_view.return_value.get_credentials.return_value = (
        "test_username",
        "test_password",
    )
    mock_service.return_value.login.return_value = (
        MagicMock(username="test_username"),
        True,
    )

    user_controller.login()

    mock_service.return_value.login.assert_called_once_with(
        username="test_username", password="test_password"
    )
    mock_view.return_value.clear_screen.assert_called_once()
    mock_view.return_value.show_message.assert_called_once()


def test_login_failure(
    user_controller: UserController, mock_service: MagicMock, mock_view: MagicMock
) -> None:
    """Test case for user login failure."""
    mock_view.return_value.get_credentials.return_value = (
        "test_username",
        "test_password",
    )
    mock_service.return_value.login.return_value = (
        MagicMock(username="test_username"),
        False,
    )

    user_controller.login()

    mock_service.return_value.login.assert_called_once_with(
        username="test_username", password="test_password"
    )
    mock_view.return_value.clear_screen.assert_called_once()
    mock_view.return_value.show_message.assert_called_once()


def test_show_welcome_msg(
    user_controller: UserController, mock_view: MagicMock
) -> None:
    """Test case for showing welcome message."""
    user_controller.show_welcome_msg()

    mock_view.return_value.clear_screen.assert_called_once()
    mock_view.return_value.show_message.assert_called_once()
