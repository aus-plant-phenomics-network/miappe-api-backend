import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model import Base

__all__ = ("Experiment",)

if TYPE_CHECKING:
    from src.model.facility import Facility
    from src.model.study import Study
    from src.model.vocabulary import Vocabulary

experiment_to_facility_table = Table(
    "experiment_to_facility_table",
    Base.metadata,
    Column("experiment_id", UUID_SQL, ForeignKey("experiment_table.id"), primary_key=True),
    Column("facility_id", UUID_SQL, ForeignKey("facility_table.id"), primary_key=True),
)


class Experiment(Base):
    __tablename__ = "experiment_table"  # type: ignore[assignment]
    objective: Mapped[str | None]
    start_date: Mapped[datetime.datetime | None]
    end_date: Mapped[datetime.datetime | None]
    observation_unit_level_hierarchy: Mapped[str | None]
    observation_unit_level_description: Mapped[str | None]
    cultural_practices: Mapped[str | None]
    map_of_exp_design: Mapped[str | None]

    # Relationship
    # facilities: Mapped[list["Facility"]] = relationship(
    #     "Facility",
    #     secondary="experiment_to_facility_table",
    #     back_populates="experiments",
    #     lazy="selectin",
    #     info=dto_field("read-only"),
    # )

    experiment_type_id: Mapped[UUID | None] = mapped_column(ForeignKey("vocabulary_table.id"))
    # experiment_type: Mapped[Optional["Vocabulary"]] = relationship(
    #     "Vocabulary", back_populates="experiment", lazy="selectin", info=dto_field("read-only")
    # )

    study_id: Mapped[UUID | None] = mapped_column(ForeignKey("study_table.id"))
    # study: Mapped[Optional["Study"]] = relationship(
    #     "Study", back_populates="experiments", lazy="selectin", info=dto_field("read-only")
    # )
