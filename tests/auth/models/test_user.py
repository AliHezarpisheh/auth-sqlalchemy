"""Unit tests for the User model class."""

from datetime import datetime

from sqlalchemy.orm import Session

from auth.models.user import User


def test_user_str(db_session: Session) -> None:
    """
    Test the string representation of the User model.

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
