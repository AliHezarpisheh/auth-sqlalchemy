"""Unit tests for the User DAL class."""

from typing import Generator
from unittest.mock import patch

import pytest
from sqlalchemy.orm import Session

from auth.models import User
from auth.repository.dal import UserDataAccessLayer
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
def user(db_session: Session) -> User:
    """Fixture for creating a user instance."""
    user = User(username="test_username", password="test_password")
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def user_dal() -> UserDataAccessLayer:
    """Fixture for instantiating a UserDataAccessLayer."""
    return UserDataAccessLayer()


def test_get_existing_user(user_dal: UserDataAccessLayer, user: User) -> None:
    """Test retrieving an existing user by username."""
    retrieved_user = user_dal.get_user_by_username(username=user.username)

    assert retrieved_user == user


def test_get_non_existing_user(user_dal: UserDataAccessLayer) -> None:
    """Test retrieving a non-existing user by username."""
    retrieved_user = user_dal.get_user_by_username(username="I am not existed")

    assert retrieved_user is None
