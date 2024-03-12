import datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from miappe.model.base import Base
from miappe.model.vocabulary import Vocabulary

if TYPE_CHECKING:
    from miappe.model import Vocabulary


class Device(Base):
    __tablename__ = "device_table"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    device_type_id: Mapped[UUID] = mapped_column(ForeignKey("vocabulary_table.id"))

    description: Mapped[Optional[str]]
    brand: Mapped[Optional[str]]
    serial_number: Mapped[Optional[str]]
    constructor_model: Mapped[Optional[str]]
    startup_date: Mapped[Optional[datetime.datetime]]
    removal_date: Mapped[Optional[datetime.datetime]]

    # Relationships:
    device_type: Mapped["Vocabulary"] = relationship(back_populates="device")

    def __repr__(self) -> str:
        return f"id: {self.id}, name: {self.name}, description: {self.description}"
