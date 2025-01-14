from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.base import Base

__all__ = ("Method",)


if TYPE_CHECKING:
    from src.model.device import Device
    from src.model.observed_variable import ObservedVariable
    from src.model.vocabulary import Vocabulary


class Method(Base):
    __tablename__: str = "method_table"
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)

    # Relationships:
    method_reference_id: Mapped[UUID | None] = mapped_column(ForeignKey("vocabulary_table.id", ondelete="SET NULL"))
    method_reference: Mapped[Optional["Vocabulary"]] = relationship(
        back_populates="method",
        lazy=None,
        info=dto_field("read-only"),
    )

    device_id: Mapped[UUID | None] = mapped_column(ForeignKey("device_table.id", ondelete="SET NULL"))
    device: Mapped[Optional["Device"]] = relationship(lazy=None, info=dto_field("read-only"))
    observed_variable: Mapped[Optional["ObservedVariable"]] = relationship(
        lazy=None, info=dto_field("read-only"), back_populates="method"
    )
