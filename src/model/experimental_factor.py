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


# TODO: make experimental factor values actual table
class ExperimentalFactor(Variable):
    __tablename__: str = "experimental_factor_table"
    __mapper_args__ = {"polymorphic_identity": "experimental_factor"}

    id: Mapped[UUID] = mapped_column(ForeignKey("variable_table.id"), primary_key=True, info=dto_field("read-only"))
    factor_values: Mapped[str]
    factor_description: Mapped[str]
    factor_type_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "vocabulary_table.id",
            ondelete="SET NULL",
        )
    )
    factor_type: Mapped[Optional["Vocabulary"]] = relationship(
        "Vocabulary",
        back_populates="factor_type",
        lazy=None,
        info=dto_field("private"),
    )

    observation_unit: Mapped[list["ObservationUnit"]] = relationship(
        "ObservationUnit",
        back_populates="biological_material",
        lazy=None,
        info=dto_field("read-only"),
    )


@dataclass(kw_only=True)
class ExperimentalFactorDataclass(VariableDataclass):
    factor_values: str | None = field(default=None)
    factor_description: str | None = field(default=None)
    factor_type_id: UUID | None = field(default=None)
