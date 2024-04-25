"""Define the User class for database ORM mapping."""

from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column

from config.database.mixins import CommonMixin
from config.database.orm import Base


class User(Base, CommonMixin):
    """Represents a user entity in the authentication system."""

    __tablename__ = "auth_user"

    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)

    last_login: Mapped[datetime] = mapped_column(nullable=True)
    date_joined: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))

    # def __str__(self) -> str:
    #     """
    #     Return a human-readable string representation of the user.

    #     Returns
    #     -------
    #     str
    #         A string containing username, last login, and date joined.
    #     """
    #     return (
    #         f"<User(username={self.username}, last_login={self.last_login}, "
    #         f"date_joined={self.date_joined})>"
    #     )

    # def __repr__(self) -> str:
    #     """
    #     Return an unambiguous string representation of the user.

    #     Returns
    #     -------
    #     str
    #         A string containing the class name and attribute values.
    #     """
    #     return (
    #         f"User(username={self.username}, last_login={self.last_login}, "
    #         f"date_joined={self.date_joined})"
    #     )
