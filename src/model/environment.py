from dataclasses import dataclass, field
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.model.variable import Variable, VariableDataclass

__all__ = ("Environment",)


class Environment(Variable):
    __tablename__: str = "environment_table"  # type: ignore[assignment]

    __mapper_args__ = {"polymorphic_identity": "environment"}

    id: Mapped[UUID] = mapped_column(ForeignKey("variable_table.id"), primary_key=True, info=dto_field("read-only"))
    setpoint: Mapped[str | None]


@dataclass
class EnvironmentDataclass(VariableDataclass):
    setpoint: str | None = field(default=None)
