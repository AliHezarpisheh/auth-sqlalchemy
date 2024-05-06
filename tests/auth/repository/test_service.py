"""Unit tests for the UserService class."""

from datetime import datetime
from typing import Generator
from unittest.mock import patch

import pytest
from sqlalchemy.orm import Session

from auth.repository.service import UserService
from config.base import db


@pytest.fixture(autouse=True)
def mock_session(db_session: Session) -> Generator[None, None, None]:
    """
    Mock the database session with the test database session.

    This fixture replaces the session object used in the application with the session
    object using the test database. It ensures that database operations performed during
    testing are isolated and do not affect the actual database.

    Parameters
    ----------
    db_session : Session
        The test database session.

    Yields
    ------
    None
    """
    with patch.object(db, "get_session") as actual_session:
        actual_session.return_value = db_session
        yield


@pytest.fixture
def user_service() -> UserService:
    """Fixture for instantiating a UserService."""
    return UserService()


def test_register(user_service: UserService) -> None:
    """Test valid register functionality."""
    username = "test_user"
    password = "test_password"
    user = user_service.register(username, password)

    assert user.username == username

    hashed_password = user_service.hash_password(password)
    assert user.password == hashed_password
    assert isinstance(user.date_joined, datetime)
    assert user.last_login is None


def test_valid_login(user_service: UserService) -> None:
    """Test valid login functionality."""
    username = "test_user"
    password = "test_password"
    user_service.register(username, password)

    user, is_authenticated = user_service.login(username, password)
    assert is_authenticated
    assert user.username == username

    hashed_password = user_service.hash_password(password)
    assert user.password == hashed_password
    assert isinstance(user.date_joined, datetime)


def test_invalid_login(user_service: UserService) -> None:
    """Test invalid login functionality."""
    username = "test_user"
    password = "test_password"
    user_service.register(username, password)

    user, is_authenticated = user_service.login("invalid username", password)
    assert not is_authenticated
    assert user is None

    user, is_authenticated = user_service.login(username, "invalid password")
    assert not is_authenticated


def test_verify_password(user_service: UserService) -> None:
    """Test password verification functionality."""
    password = "test_password"
    hashed_password = user_service.hash_password(password)
    assert user_service.verify_password(password, hashed_password)

    assert not user_service.verify_password(password, password)
    assert not user_service.verify_password("invalid password", hashed_password)
    assert not user_service.verify_password("invalid password", "invalid password")
