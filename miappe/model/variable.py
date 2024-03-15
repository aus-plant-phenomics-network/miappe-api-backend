from typing import TYPE_CHECKING, Optional
from uuid import UUID
from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from miappe.model.base import Base

if TYPE_CHECKING:
    from miappe.model.biological_material import BiologicalMaterial
    from miappe.model.vocabulary import Device, Vocabulary


class Variable(Base):
    __tablename__: str = "variable_table"  # type: ignore

    time_interval: Mapped[Optional[str]]
    sample_interval: Mapped[Optional[str]]

    # Relationships:
    variable_type_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("vocabulary_table.id")
    )
    variable_type: Mapped[Optional["Vocabulary"]] = relationship(
        back_populates="variable", lazy="selectin", info=dto_field("read-only")
    )

    device_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("device_table.id"))
    device: Mapped[Optional["Device"]] = relationship(
        back_populates="variable", lazy="selectin", info=dto_field("read-only")
    )

    # Sub-variable relationship
    biological_material: Mapped[Optional["BiologicalMaterial"]] = relationship(
        back_populates="variable", lazy="selectin", info=dto_field("read-only")
    )

    # TODO: Add study information
