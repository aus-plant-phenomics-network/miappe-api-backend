from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.variable import Variable, VariableDataclass

__all__ = ("ObservedVariable",)


if TYPE_CHECKING:
    from src.model.method import Method
    from src.model.vocabulary import Vocabulary


class ObservedVariable(Variable):
    __tablename__: str = "observed_variable_table"
    __mapper_args__ = {"polymorphic_identity": "observed_variable"}
    id: Mapped[UUID] = mapped_column(ForeignKey("variable_table.id"), primary_key=True, info=dto_field("read-only"))

    title: Mapped[str] = mapped_column(nullable=False)
    method_id: Mapped[UUID | None] = mapped_column(ForeignKey("method_table.id", ondelete="SET NULL"))
    method: Mapped[Optional["Method"]] = relationship(
        "Method",
        lazy=None,
        back_populates="observed_variable",
        info=dto_field("read-only"),
    )
    trait_reference_id: Mapped[UUID | None] = mapped_column(ForeignKey("vocabulary_table.id", ondelete="SET NULL"))
    trait_reference: Mapped[Optional["Vocabulary"]] = relationship(
        "Vocabulary",
        lazy=None,
        back_populates="trait_reference",
        info=dto_field("read-only"),
        foreign_keys=[trait_reference_id],
    )


@dataclass(kw_only=True)
class ObservedVariableDataclass(VariableDataclass):
    title: str
    method_id: UUID | None = field(default=None)
    trait_reference_id: UUID | None = field(default=None)
