import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.base import Base

__all__ = ("Device",)

if TYPE_CHECKING:
    from src.model.vocabulary import Vocabulary


class Device(Base):
    __tablename__: str = "device_table"  # type: ignore[assignment]
    name: Mapped[str] = mapped_column(nullable=False)
    brand: Mapped[str | None]
    serial_number: Mapped[str | None]
    constructor_model: Mapped[str | None]
    startup_date: Mapped[datetime.datetime | None]
    removal_date: Mapped[datetime.datetime | None]

    # Relationships:
    # With vocabulary
    device_type_id: Mapped[UUID | None] = mapped_column(ForeignKey("vocabulary_table.id", ondelete="SET NULL"))
    device_type: Mapped[Optional["Vocabulary"]] = relationship(
        back_populates="device", lazy=None, info=dto_field("read-only")
    )
