import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.base import Base

if TYPE_CHECKING:
    from src.model.method import Method
    from src.model.variable import Variable
    from src.model.vocabulary import Vocabulary


class Device(Base):
    __tablename__: str = "device_table"  # type: ignore

    brand: Mapped[Optional[str]]
    serial_number: Mapped[Optional[str]]
    constructor_model: Mapped[Optional[str]]
    startup_date: Mapped[Optional[datetime.datetime]]
    removal_date: Mapped[Optional[datetime.datetime]]

    # Relationships:
    # With vocabulary
    device_type_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("vocabulary_table.id")
    )
    device_type: Mapped[Optional["Vocabulary"]] = relationship(
        back_populates="device", lazy="selectin", info=dto_field("read-only")
    )

    # With method
    method: Mapped[list["Method"]] = relationship(
        back_populates="device", lazy="selectin", info=dto_field("read-only")
    )

    # With variable
    variable: Mapped[list["Variable"]] = relationship(
        back_populates="device", lazy="selectin", info=dto_field("read-only")
    )
