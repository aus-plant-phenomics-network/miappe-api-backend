import datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from miappe.model.base import Base

if TYPE_CHECKING:
    from miappe.model.method import Method
    from miappe.model.vocabulary import Vocabulary
    from miappe.model.variable import Variable


class Device(Base):
    __tablename__ = "device_table"

    brand: Mapped[Optional[str]]
    serial_number: Mapped[Optional[str]]
    constructor_model: Mapped[Optional[str]]
    startup_date: Mapped[Optional[datetime.datetime]]
    removal_date: Mapped[Optional[datetime.datetime]]

    # Relationships:
    # With vocabulary
    device_type_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("vocabulary_table.id"))
    device_type: Mapped[Optional["Vocabulary"]] = relationship(back_populates="device", lazy="selectin")

    # With method
    method: Mapped[Optional[list["Method"]]] = relationship(back_populates="device", lazy="selectin")

    # With variable
    variable: Mapped[Optional[list["Variable"]]] = relationship(back_populates="device", lazy="selectin")