from typing import Optional, TYPE_CHECKING
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from miappe.model import Base

if TYPE_CHECKING:
    from miappe.model.unit import Unit
    from miappe.model.variable import Variable


class Environment(Base):
    __tablename__: str = "environment_table"  # type: ignore

    id: Mapped[UUID] = mapped_column(
        ForeignKey("variable_table.id"), primary_key=True, info=dto_field("read-only")
    )
    set_point: Mapped[Optional[str]]
    unit_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("unit_table.id"))

    # Relationship
    unit: Mapped[Optional["Unit"]] = relationship(
        "Unit",
        back_populates="environment",
        lazy="selectin",
        info=dto_field("read-only"),
    )
    variable: Mapped["Variable"] = relationship(
        "Variable",
        back_populates="environment",
        lazy="selectin",
        info=dto_field("read-only"),
    )
