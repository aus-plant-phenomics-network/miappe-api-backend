from typing import Optional, TYPE_CHECKING
from uuid import UUID
from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from miappe.model.base import Base

if TYPE_CHECKING:
    from miappe.model.method import Method
    from miappe.model.variable import Variable


class BiologicalMaterial(Base):
    __tablename__: str = "biological_material_table"  # type: ignore

    id: Mapped[UUID] = mapped_column(
        ForeignKey("variable_table.id"), primary_key=True, info=dto_field("read-only")
    )
    biological_location: Mapped[Optional[str]]
    material_source_id: Mapped[Optional[str]]
    material_source_doi: Mapped[Optional[str]]
    material_source_location: Mapped[Optional[str]]
    material_source_description: Mapped[Optional[str]]

    # Relationship
    preprocessing_method_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("method_table.id")
    )
    preprocessing_method: Mapped[Optional["Method"]] = relationship(
        back_populates="biological_material",
        lazy="selectin",
        info=dto_field("read-only"),
    )
    variable: Mapped["Variable"] = relationship(
        back_populates="biological_material",
        lazy="selectin",
        info=dto_field("read-only"),
    )
