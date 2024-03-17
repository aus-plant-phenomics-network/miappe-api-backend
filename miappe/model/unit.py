from typing import Optional, TYPE_CHECKING
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from miappe.model.base import Base

if TYPE_CHECKING:
    from miappe.model.vocabulary import Vocabulary
    from miappe.model.environment import Environment
    from miappe.model.observed_variable import ObservedVariable
    from miappe.model.experimental_factor import ExperimentalFactor

class Unit(Base):
    __tablename__ = "unit_table"  # type: ignore

    symbol: Mapped[Optional[str]]
    alternative_symbol: Mapped[Optional[str]]

    # Relationships:
    unit_type_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("vocabulary_table.id")
    )
    unit_type: Mapped[Optional["Vocabulary"]] = relationship(
        "Vocabulary",
        back_populates="unit",
        lazy="selectin",
        info=dto_field("read-only"))
    environment: Mapped[list["Environment"]] = relationship(
        "Environment",
        back_populates="unit",
        lazy="selectin",
        info=dto_field("read-only"))
    observed_variable: Mapped[list["ObservedVariable"]] = relationship(
        "ObservedVariable",
        back_populates="unit",
        lazy="selectin",
        info=dto_field("read-only"))
    experimental_factor: Mapped[list["ExperimentalFactor"]] = relationship(
        "ExperimentalFactor",
        back_populates="unit",
        lazy="selectin",
        info=dto_field("read-only")
    )