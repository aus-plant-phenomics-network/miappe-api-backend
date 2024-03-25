from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model import Base

__all__ = ("ObservedVariable",)


if TYPE_CHECKING:
    from src.model.method import Method
    from src.model.unit import Unit


class ObservedVariable(Base):
    __tablename__: str = "observed_variable_table"  # type: ignore

    id: Mapped[UUID] = mapped_column(ForeignKey("variable_table.id"), primary_key=True, info=dto_field("read-only"))
    method_id: Mapped[UUID | None] = mapped_column(ForeignKey("method_table.id"))
    unit_id: Mapped[UUID | None] = mapped_column(ForeignKey("unit_table.id"))

    # Relationship
    method: Mapped[Optional["Method"]] = relationship(
        back_populates="observed_variable", lazy="selectin", info=dto_field("read-only")
    )
    unit: Mapped[Optional["Unit"]] = relationship(
        back_populates="observed_variable", lazy="selectin", info=dto_field("read-only")
    )
