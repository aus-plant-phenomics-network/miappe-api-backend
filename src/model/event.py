import datetime
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, cast
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.base import Base, BaseDataclass, Serialisable

if TYPE_CHECKING:
    from src.model.observation_unit import ObservationUnit
    from src.model.study import Study
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
    title: Mapped[str]
    description: Mapped[str | None]
    event_date: Mapped[datetime.datetime | None]
    event_type_id: Mapped[UUID | None] = mapped_column(
        ForeignKey(
            "vocabulary_table.id",
            ondelete="SET NULL",
        ),
    )

    # Relationship
    event_type: Mapped[Optional["Vocabulary"]] = relationship(
        lazy=None,
        info=dto_field("read-only"),
        back_populates="event",
    )
    observation_units: Mapped[list["ObservationUnit"]] = relationship(
        secondary="event_to_ob_unit_table",
        lazy=None,
        info=dto_field("read-only"),
        back_populates="events",
    )
    studies: Mapped[list["Study"]] = relationship(
        secondary="event_to_study_table",
        lazy=None,
        info=dto_field("read-only"),
        back_populates="events",
    )


@dataclass(kw_only=True)
class EventDataclass(BaseDataclass):
    title: str
    description: str | None = field(default=None)
    event_date: datetime.datetime | None = field(default=None)
    event_type_id: UUID | None = field(default=None)
    observation_unit_id: list[UUID] = field(default_factory=list[UUID])
    study_id: list[UUID] = field(default_factory=list[UUID])

    @classmethod
    def from_orm(cls, data: Serialisable) -> "BaseDataclass":
        data = cast(Event, data)
        data_dict = data.to_dict()
        if len(data.observation_units) > 0:
            data_dict["observation_unit_id"] = [item.id for item in data.observation_units]
        if len(data.studies) > 0:
            data_dict["study_id"] = [item.id for item in data.studies]
        return cls(**data_dict)
