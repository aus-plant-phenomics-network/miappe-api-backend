import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model import Base

__all__ = ("Study",)

if TYPE_CHECKING:
    from src.model.data_file import DataFile
    from src.model.event import Event
    from src.model.experiment import Experiment
    from src.model.investigation import Investigation
    from src.model.observation_unit import ObservationUnit
    from src.model.variable import Variable


class Study(Base):
    __tablename__ = "study_table"
    title: Mapped[str] = mapped_column(nullable=False)
    objective: Mapped[str] = mapped_column(nullable=False)
    start_date: Mapped[datetime.datetime] = mapped_column(nullable=False)
    end_date: Mapped[datetime.datetime | None]

    # Relationship
    investigation_id: Mapped[UUID] = mapped_column(ForeignKey("investigation_table.id", ondelete="cascade"))
    investigation: Mapped[Optional["Investigation"]] = relationship(
        lazy=None,
        info=dto_field("read-only"),
        back_populates="studies",
    )
    variables: Mapped[list["Variable"]] = relationship(
        secondary="study_variable_table",
        lazy=None,
        info=dto_field("read-only"),
        back_populates="studies",
    )
    data_files: Mapped[list["DataFile"]] = relationship(
        secondary="study_data_file_table",
        lazy=None,
        info=dto_field("read-only"),
        back_populates="studies",
    )
    experiments: Mapped[list["Experiment"]] = relationship(
        lazy=None,
        info=dto_field("read-only"),
        back_populates="study",
    )
    observation_unit: Mapped[list["ObservationUnit"]] = relationship(
        secondary="ob_unit_to_study_table",
        lazy=None,
        info=dto_field("read-only"),
        back_populates="studies",
    )
    events: Mapped[list["Event"]] = relationship(
        secondary="event_to_study_table",
        lazy=None,
        info=dto_field("read-only"),
        back_populates="studies",
    )
