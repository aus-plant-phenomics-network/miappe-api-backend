from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model import Base

__all__ = ("Environment",)


if TYPE_CHECKING:
    from src.model.unit import Unit
    from src.model.variable import Variable


class Environment(Base):
    __tablename__: str = "environment_table"  # type: ignore[assignment]

    id: Mapped[UUID] = mapped_column(ForeignKey("variable_table.id"), primary_key=True, info=dto_field("read-only"))
    set_point: Mapped[str | None]
    unit_id: Mapped[UUID | None] = mapped_column(ForeignKey("unit_table.id"))

    # Relationship
    unit: Mapped[Optional["Unit"]] = relationship(
        "Unit",
        lazy="selectin",
        info=dto_field("read-only"),
    )
    variable: Mapped["Variable"] = relationship(
        "Variable",
        back_populates="environment",
        lazy="selectin",
        info=dto_field("read-only"),
    )
