from dataclasses import dataclass, field
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.model.variable import Variable, VariableDataclass

__all__ = ("ExperimentalFactor",)


# TODO: make experimental factor values actual table
class ExperimentalFactor(Variable):
    __tablename__: str = "experimental_factor_table"  # type: ignore[assignment]
    __mapper_args__ = {"polymorphic_identity": "experimental_factor"}

    id: Mapped[UUID] = mapped_column(ForeignKey("variable_table.id"), primary_key=True, info=dto_field("read-only"))
    factor_values: Mapped[str]


@dataclass(kw_only=True)
class ExperimentalFactorDataclass(VariableDataclass):
    factor_values: str | None = field(default=None)
