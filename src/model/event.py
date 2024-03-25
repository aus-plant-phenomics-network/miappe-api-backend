import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model import Base

__all__ = ("Event",)


if TYPE_CHECKING:
    from src.model.observation_unit import ObservationUnit
    from src.model.vocabulary import Vocabulary


class Event(Base):
    __tablename__ = "event_table"  # type: ignore[assignment]
    event_date: Mapped[datetime.datetime | None]
    vocabulary_id: Mapped[UUID | None] = mapped_column(ForeignKey("vocabulary_table.id"))
    observation_unit_id: Mapped[UUID | None] = mapped_column(ForeignKey("observation_unit_table.id"))

    # Relationship
    event_type: Mapped[Optional["Vocabulary"]] = relationship(
        "Vocabulary", back_populates="event", lazy="selectin", info=dto_field("read-only")
    )
    observation_unit: Mapped[Optional["ObservationUnit"]] = relationship(
        "ObservationUnit", back_populates="event", lazy="selectin", info=dto_field("read-only")
    )
