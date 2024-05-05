from typing import Generator
from unittest.mock import patch

import pytest
from sqlalchemy.orm import Session

from auth.models import User
from auth.repository.dal import UserDataAccessLayer
from config.base import db


@pytest.fixture(autouse=True)
def mock_session(db_session: Session) -> Generator[None, None, None]:
    with patch.object(db, "get_session") as actual_session:
        actual_session.return_value = db_session
        yield


@pytest.fixture
def user(db_session: Session) -> User:
    user = User(username="test_username", password="test_password")
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def user_dal() -> UserDataAccessLayer:
    return UserDataAccessLayer()


def test_get_existing_user(user_dal: UserDataAccessLayer, user: User) -> None:
    retrieved_user = user_dal.get_user_by_username(username=user.username)

    assert retrieved_user == user


def test_get_non_existing_user(user_dal: UserDataAccessLayer) -> None:
    retrieved_user = user_dal.get_user_by_username(username="I am not existed")

    assert retrieved_user is None
