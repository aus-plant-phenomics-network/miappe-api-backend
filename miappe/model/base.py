from datetime import datetime, timezone
from uuid import UUID, uuid4

from advanced_alchemy.base import CommonTableAttributes
from advanced_alchemy.types import DateTimeUTC
from litestar.dto import dto_field
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(CommonTableAttributes, DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        default=uuid4, primary_key=True, info=dto_field("read-only")
    )
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)

    # Audit columns - read-only
    created_at: Mapped[datetime] = mapped_column(
        DateTimeUTC(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        info=dto_field("read-only"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTimeUTC(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        info=dto_field("read-only"),
    )

    def __repr__(self) -> str:
        return f"id: {self.id}, name: {self.name}, description: {self.description}"
