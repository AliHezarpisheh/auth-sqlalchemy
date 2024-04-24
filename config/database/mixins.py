"""Contains database mixins for common functionalities."""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    """A mixin class to add created_at and modified_at timestamp fields."""

    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    modified_at: Mapped[Optional[datetime]] = mapped_column(
        default=None, nullable=True, onupdate=datetime.now(timezone.utc)
    )
