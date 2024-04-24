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
