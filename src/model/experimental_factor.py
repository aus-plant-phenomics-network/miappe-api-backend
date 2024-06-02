from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.variable import Variable, VariableDataclass

if TYPE_CHECKING:
    from src.model.observation_unit import ObservationUnit
    from src.model.vocabulary import Vocabulary

__all__ = ("ExperimentalFactor",)


class ExperimentalFactor(Variable):
    __tablename__: str = "experimental_factor_table"
    __mapper_args__ = {"polymorphic_identity": "experimental_factor"}

    id: Mapped[UUID] = mapped_column(
        ForeignKey("variable_table.id", ondelete="cascade"),
        primary_key=True,
        info=dto_field("read-only"),
    )
    title: Mapped[str]
    factor_value: Mapped[str]
    factor_description: Mapped[str]
    factor_type_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "vocabulary_table.id",
            ondelete="SET NULL",
        )
    )
    factor_type: Mapped[Optional["Vocabulary"]] = relationship(
        back_populates="factor_type",
        lazy=None,
        info=dto_field("private"),
    )

    observation_units: Mapped[list["ObservationUnit"]] = relationship(
        secondary="ob_unit_to_exp_factor_table",
        back_populates="experimental_factors",
        lazy=None,
        info=dto_field("read-only"),
    )


@dataclass(kw_only=True)
class ExperimentalFactorDataclass(VariableDataclass):
    title: str
    factor_value: str
    factor_description: str | None = field(default=None)
    factor_type_id: UUID | None = field(default=None)
