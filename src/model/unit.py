from typing import Optional, TYPE_CHECKING
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.base import Base

if TYPE_CHECKING:
    from src.model.vocabulary import Vocabulary
    from src.model.environment import Environment
    from src.model.observed_variable import ObservedVariable
    from src.model.experimental_factor import ExperimentalFactor

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