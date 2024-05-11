from datetime import UTC, datetime
from uuid import UUID, uuid4

from advanced_alchemy.base import CommonTableAttributes
from advanced_alchemy.types import DateTimeUTC
from litestar.dto import dto_field
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

__all__ = ("Base",)


class Base(CommonTableAttributes, DeclarativeBase):
    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True, info=dto_field("read-only"))
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(nullable=True)

    # Audit columns - read-only
    created_at: Mapped[datetime] = mapped_column(
        DateTimeUTC(timezone=True),
        default=lambda: datetime.now(UTC),
        info=dto_field("read-only"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTimeUTC(timezone=True),
        default=lambda: datetime.now(UTC),
        info=dto_field("read-only"),
    )

    def __repr__(self) -> str:
        return f"id: {self.id}, name: {self.title}, description: {self.description}"
