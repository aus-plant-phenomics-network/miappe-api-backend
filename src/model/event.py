import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model import Base

if TYPE_CHECKING:
    from src.model.observation_unit import ObservationUnit
    from src.model.vocabulary import Vocabulary

__all__ = ("Event",)


event_to_ob_unit_table = Table(
    "event_to_ob_unit_table",
    Base.metadata,
    Column("event_id", UUID_SQL, ForeignKey("event_table.id", ondelete="cascade"), primary_key=True),
    Column(
        "observation_unit_id", UUID_SQL, ForeignKey("observation_unit_table.id", ondelete="cascade"), primary_key=True
    ),
)

event_to_study_table = Table(
    "event_to_study_table",
    Base.metadata,
    Column("event_id", UUID_SQL, ForeignKey("event_table.id", ondelete="cascade"), primary_key=True),
    Column("study_id", UUID_SQL, ForeignKey("study_table.id", ondelete="cascade"), primary_key=True),
)


class Event(Base):
    __tablename__ = "event_table"
    event_date: Mapped[datetime.datetime | None]
    event_type_id: Mapped[UUID | None] = mapped_column(ForeignKey("vocabulary_table.id", ondelete="SET NULL"))

    # Relationship
    event_type: Mapped[Optional["Vocabulary"]] = relationship(
        "Vocabulary",
        back_populates="event",
        lazy=None,
        info=dto_field("read-only"),
    )
    observation_unit: Mapped[list["ObservationUnit"]] = relationship(
        "ObservationUnit",
        secondary="event_to_ob_unit_table",
        back_populates="events",
        lazy=None,
        info=dto_field("read-only"),
    )
