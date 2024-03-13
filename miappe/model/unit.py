from typing import Optional, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from miappe.model.base import Base

if TYPE_CHECKING:
    from miappe.model.vocabulary import Vocabulary


class Unit(Base):
    __tablename__ = "unit_table"

    symbol: Mapped[Optional[str]]
    alternative_symbol: Mapped[Optional[str]]

    # Relationships:
    unit_type_id: Mapped[UUID] = mapped_column(ForeignKey("vocabulary_table.id"), nullable=True)
    unit_type: Mapped["Vocabulary"] = relationship(back_populates="unit", lazy="selectin")
