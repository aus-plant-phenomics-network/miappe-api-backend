from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from miappe.model.base import Base

if TYPE_CHECKING:
    from miappe.model.vocabulary import Vocabulary


class Unit(Base):
    __tablename__ = "unit_table"  # type: ignore

    symbol: Mapped[Optional[str]]
    alternative_symbol: Mapped[Optional[str]]

    # Relationships:
    unit_type_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("vocabulary_table.id")
    )
    unit_type: Mapped[Optional["Vocabulary"]] = relationship(
        back_populates="unit", lazy="selectin", info=dto_field("read-only")
    )
