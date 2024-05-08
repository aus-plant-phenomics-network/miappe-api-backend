from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.base import Base

__all__ = ("Unit",)

if TYPE_CHECKING:
    from src.model.vocabulary import Vocabulary


class Unit(Base):
    __tablename__ = "unit_table"  # type: ignore[assignment]

    symbol: Mapped[str | None]
    alternative_symbol: Mapped[str | None]

    # Relationships:
    unit_type_id: Mapped[UUID | None] = mapped_column(ForeignKey("vocabulary_table.id"))
    unit_type: Mapped[Optional["Vocabulary"]] = relationship(
        "Vocabulary", back_populates="unit", lazy="selectin", info=dto_field("read-only")
    )
