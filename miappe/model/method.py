from typing import Optional, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from miappe.model.base import Base

if TYPE_CHECKING:
    from miappe.model.device import Device
    from miappe.model.vocabulary import Vocabulary
    from miappe.model.biological_material import BiologicalMaterial


class Method(Base):
    __tablename__ = "method_table"

    # Relationships:
    method_type_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("vocabulary_table.id"))
    method_type: Mapped["Vocabulary"] = relationship(back_populates="method", lazy="selectin")

    device_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("device_table.id"))
    device: Mapped["Device"] = relationship(back_populates="method", lazy="selectin")

    biological_material: Mapped[Optional["BiologicalMaterial"]] = relationship(back_populates="preprocessing_method",
                                                                               lazy="selectin")