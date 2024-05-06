"""Unit tests for the User BLL class."""

from typing import Generator
from unittest.mock import patch

import pytest
from sqlalchemy.orm import Session

from auth.helpers.exceptions import UserAlreadyExistsError
from auth.models import User
from auth.repository.bll import UserBusinessLogicLayer
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
def user_bll() -> UserBusinessLogicLayer:
    """Fixture for instantiating a UserBusinessLogicLayer."""
    return UserBusinessLogicLayer()


@pytest.mark.parametrize(
    "username, password",
    [
        ("valid_username", "valid_password"),
        ("", "valid_password"),
        ("valid_username", ""),
        ("u", "p"),
        ("a" * 50, "b" * 50),
        ("!@#$%^&*", "!@#$%^&*"),
    ],
    ids=[
        "valid_credentials",
        "empty_username",
        "empty_password",
        "short_credentials",
        "long_credentials",
        "special_characters_credentials",
    ],
)
@pytest.mark.smoke
def test_create_user(
    user_bll: UserBusinessLogicLayer,
    username: str,
    password: str,
    db_session: Session,
) -> None:
    """
    Test case for creating a user.

    Parameters
    ----------
    user_bll : UserBusinessLogicLayer
        The instance of UserBusinessLogicLayer.
    username : str
        The username of the user to be created.
    password : str
        The password of the user to be created.
    db_session : Session
        The database session.
    """
    user = user_bll.create_user(username=username, password=password)

    retrieved_user = db_session.query(User).filter_by(username=username).first()
    assert user.username == retrieved_user.username
    assert user.password == retrieved_user.password


@pytest.mark.exception
def test_create_duplicate_user(user_bll: UserBusinessLogicLayer) -> None:
    """
    Test case for creating a duplicate user.

    Parameters
    ----------
    user_bll : UserBusinessLogicLayer
        The instance of UserBusinessLogicLayer.
    """
    user_bll.create_user(username="test_username", password="test_password")

    with pytest.raises(
        UserAlreadyExistsError, match="User test_username Already Registered."
    ):
        user_bll.create_user(username="test_username", password="another_password")
