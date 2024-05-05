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
    with patch.object(db, "get_session") as actual_session:
        actual_session.return_value = db_session
        yield


@pytest.fixture
def user_bll() -> UserBusinessLogicLayer:
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
)
@pytest.mark.smoke
def test_create_user(
    user_bll: UserBusinessLogicLayer,
    username: str,
    password: str,
    db_session: Session,
) -> None:
    user = user_bll.create_user(username=username, password=password)

    retrieved_user = db_session.query(User).filter_by(username=username).first()
    assert user.username == retrieved_user.username
    assert user.password == retrieved_user.password


@pytest.mark.exception
def test_create_duplicate_user(user_bll: UserBusinessLogicLayer) -> None:
    user_bll.create_user(username="test_username", password="test_password")

    with pytest.raises(
        UserAlreadyExistsError, match="User test_username Already Registered."
    ):
        user_bll.create_user(username="test_username", password="another_password")
