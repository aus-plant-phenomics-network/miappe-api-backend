from typing import Optional, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from miappe.model.base import Base

if TYPE_CHECKING:
    from miappe.model.vocabulary import Vocabulary, Device
    from miappe.model.biological_material import BiologicalMaterial


class Variable(Base):
    __tablename__ = "variable_table"

    time_interval: Mapped[Optional[str]]
    sample_interval: Mapped[Optional[str]]

    # Relationships:
    variable_type_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("vocabulary_table.id"))
    variable_type: Mapped[Optional["Vocabulary"]] = relationship(back_populates="variable", lazy="selectin")

    device_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("device_table.id"))
    device: Mapped[Optional["Device"]] = relationship(back_populates="variable", lazy="selectin")

    # Sub-variable relationship
    biological_material: Mapped[Optional["BiologicalMaterial"]] = relationship(back_populates="variable",
                                                                               lazy="selectin")

    # TODO: Add study information
