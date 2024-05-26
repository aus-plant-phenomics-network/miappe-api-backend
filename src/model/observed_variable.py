from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.variable import Variable

__all__ = ("ObservedVariable",)


if TYPE_CHECKING:
    from src.model.method import Method


class ObservedVariable(Variable):
    __tablename__: str = "observed_variable_table"  # type: ignore[assignment]
    __mapper_args__ = {"polymorphic_identity": "observed_variable"}

    id: Mapped[UUID] = mapped_column(ForeignKey("variable_table.id"), primary_key=True, info=dto_field("read-only"))
    method_id: Mapped[UUID | None] = mapped_column(ForeignKey("method_table.id"))
    method: Mapped[Optional["Method"]] = relationship(
        back_populates="observed_variable", lazy=None, info=dto_field("read-only")
    )
