from typing import Optional, TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship

from miappe.model.base import Base

if TYPE_CHECKING:
    from miappe.model.device import Device
    from miappe.model.method import Method
    from miappe.model.unit import Unit
    from miappe.model.variable import Variable


class Vocabulary(Base):
    __tablename__ = "vocabulary_table"

    external_reference: Mapped[Optional[str]]
    namespace: Mapped[Optional[str]] = mapped_column(server_default="APPN")  # Todo: Make namespace a separate entity?
    relationship_type: Mapped[Optional[str]]  # Todo: use the same terminologies as PHIS - extract, widening, narrowing?

    # Relationships
    device: Mapped[Optional[list["Device"]]] = relationship(back_populates="device_type", lazy="selectin")
    method: Mapped[Optional[list["Method"]]] = relationship(back_populates="method_type", lazy="selectin")
    unit: Mapped[Optional[list["Unit"]]] = relationship(back_populates="unit_type", lazy="selectin")
    variable: Mapped[Optional[list["Variable"]]] = relationship(back_populates="variable_type", lazy="selectin")
    
