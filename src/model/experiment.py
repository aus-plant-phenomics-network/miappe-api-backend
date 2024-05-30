import datetime
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, cast
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.base import Base, BaseDataclass, Serialisable

__all__ = ("Experiment",)

if TYPE_CHECKING:
    from src.model.facility import Facility
    from src.model.staff import Staff
    from src.model.study import Study
    from src.model.vocabulary import Vocabulary

experiment_to_facility_table = Table(
    "experiment_to_facility_table",
    Base.metadata,
    Column("experiment_id", UUID_SQL, ForeignKey("experiment_table.id", ondelete="cascade"), primary_key=True),
    Column("facility_id", UUID_SQL, ForeignKey("facility_table.id", ondelete="cascade"), primary_key=True),
)

experiment_to_staff_table = Table(
    "experiment_to_staff_table",
    Base.metadata,
    Column("experiment_id", UUID_SQL, ForeignKey("experiment_table.id", ondelete="cascade"), primary_key=True),
    Column("staff_id", UUID_SQL, ForeignKey("staff_table.id", ondelete="cascade"), primary_key=True),
)


class Experiment(Base):
    __tablename__ = "experiment_table"  # type: ignore[assignment]
    title: Mapped[str] = mapped_column(nullable=False)
    objective: Mapped[str | None]
    start_date: Mapped[datetime.datetime | None]
    end_date: Mapped[datetime.datetime | None]
    observation_unit_level_hierarchy: Mapped[str | None]
    observation_unit_level_description: Mapped[str | None]
    cultural_practices: Mapped[str | None]
    description_of_experimental_design: Mapped[str | None]
    map_of_experimental_design: Mapped[str | None]

    # Relationship
    facilities: Mapped[list["Facility"]] = relationship(
        "Facility",
        secondary="experiment_to_facility_table",
        back_populates="experiments",
        lazy=None,
        info=dto_field("read-only"),
    )
    staffs: Mapped[list["Staff"]] = relationship(
        "Staff",
        secondary="experiment_to_staff_table",
        back_populates="experiments",
        lazy=None,
        info=dto_field("read-only"),
    )

    experiment_type_id: Mapped[UUID | None] = mapped_column(ForeignKey("vocabulary_table.id"))
    experiment_type: Mapped[Optional["Vocabulary"]] = relationship(
        "Vocabulary", back_populates="experiment", lazy=None, info=dto_field("read-only")
    )

    study_id: Mapped[UUID | None] = mapped_column(ForeignKey("study_table.id"))
    study: Mapped[Optional["Study"]] = relationship(
        "Study", back_populates="experiments", lazy=None, info=dto_field("read-only")
    )


@dataclass(kw_only=True)
class ExperimentDataclass(BaseDataclass):
    title: str
    objective: str | None = field(default=None)
    start_date: datetime.datetime | None = field(default=None)
    end_date: datetime.datetime | None = field(default=None)
    observation_unit_level_hierarchy: str | None = field(default=None)
    observation_unit_level_description: str | None = field(default=None)
    cultural_practices: str | None = field(default=None)
    map_of_experimental_design: str | None = field(default=None)
    description_of_experimental_design: str | None = field(default=None)
    experiment_type_id: UUID | None = field(default=None)
    study_id: UUID | None = field(default=None)
    facility_id: list[UUID] = field(default_factory=list[UUID])
    staff_id: list[UUID] = field(default_factory=list[UUID])

    @classmethod
    def from_orm(cls, data: Serialisable) -> "ExperimentDataclass":
        data = cast(Experiment, data)
        data_dict = data.to_dict()
        if len(data.facilities) > 0:
            data_dict["facility_id"] = [item.id for item in data.facilities]
        if len(data.staffs) > 0:
            data_dict["staff_id"] = [item.id for item in data.staffs]
        return cls(**data_dict)
