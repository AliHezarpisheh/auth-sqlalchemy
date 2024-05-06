"""Unit tests for the User model class."""

from datetime import datetime

import pytest
from sqlalchemy.orm import Session

from auth.models.user import User


@pytest.mark.smoke
def test_user_model(db_session: Session) -> None:
    """
    Test the creation and retrieval of the User model.

    Adds a user to the database session, retrieves it, and then checks its attributes.

    Parameters
    ----------
    db_session : Session
        The SQLAlchemy database session.
    """
    user = User(username="test_user", password="password")
    db_session.add(user)
    db_session.commit()

    retrieved_user = db_session.query(User).filter_by(username="test_user").first()

    assert retrieved_user is not None
    assert retrieved_user.username == "test_user"
    assert retrieved_user.password == "password"
    assert isinstance(retrieved_user.date_joined, datetime)
    assert retrieved_user.last_login is None


def test_user_str(db_session: Session) -> None:
    """
    Test the string representation of the User model.

    Parameters
    ----------
    db_session : Session
        The SQLAlchemy database session.
    """
    user = User(username="test_user", password="password")
    db_session.add(user)
    db_session.commit()

    retrieved_user = db_session.query(User).filter_by(username="test_user").first()

    expected_str = (
        f"<User(username={retrieved_user.username}, "
        f"last_login={retrieved_user.last_login}, "
        f"date_joined={retrieved_user.date_joined})>"
    )
    actual_str = str(retrieved_user)
    assert expected_str == actual_str


def test_user_repr(db_session: Session) -> None:
    """
    Test the representation of the User model.

    Parameters
    ----------
    db_session : Session
        The SQLAlchemy database session.
    """
    user = User(username="test_user", password="password")
    db_session.add(user)
    db_session.commit()

    retrieved_user = db_session.query(User).filter_by(username="test_user").first()

    expected_repr = (
        f"User(username={retrieved_user.username}, "
        f"last_login={retrieved_user.last_login}, "
        f"date_joined={retrieved_user.date_joined})"
    )
    actual_repr = repr(retrieved_user)
    assert expected_repr == actual_repr
