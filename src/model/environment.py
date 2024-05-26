from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.model.variable import Variable

__all__ = ("Environment",)


class Environment(Variable):
    __tablename__: str = "environment_table"  # type: ignore[assignment]

    __mapper_args__ = {"polymorphic_identity": "environment"}

    id: Mapped[UUID] = mapped_column(ForeignKey("variable_table.id"), primary_key=True, info=dto_field("read-only"))
    set_point: Mapped[str | None]
