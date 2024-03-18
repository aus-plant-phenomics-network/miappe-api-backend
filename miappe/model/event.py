import datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from miappe.model import Base

if TYPE_CHECKING:
    from miappe.model.vocabulary import Vocabulary
    from miappe.model.observation_unit import ObservationUnit


class Event(Base):
    __tablename__ = "event_table"  # type: ignore
    event_date: Mapped[Optional[datetime.datetime]]
    vocabulary_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("vocabulary_table.id"))
    observation_unit_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("observation_unit_table.id"))

    # Relationship
    event_type: Mapped[Optional["Vocabulary"]] = relationship(
        "Vocabulary",
        back_populates="event",
        lazy="selectin",
        info=dto_field("read-only"))
    observation_unit: Mapped[Optional["ObservationUnit"]] = relationship(
        "ObservationUnit",
        back_populates="event",
        lazy="selectin",
        info=dto_field("read-only")
    )
