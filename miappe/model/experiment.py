import datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from miappe.model import Base

if TYPE_CHECKING:
    from miappe.model.vocabulary import Vocabulary
    from miappe.model.facility import Facility
    from miappe.model.study import Study

experiment_to_facility_table = Table(
    "experiment_to_facility_table",
    Base.metadata,
    Column("experiment_id", UUID_SQL, ForeignKey("experiment_table.id"), primary_key=True),
    Column("facility_id", UUID_SQL, ForeignKey("facility_table.id"), primary_key=True),
)


class Experiment(Base):
    __tablename__ = "experiment_table"
    objective: Mapped[Optional[str]]
    start_date: Mapped[Optional[datetime.datetime]]
    end_date: Mapped[Optional[datetime.datetime]]

    # Relationship
    facilities: Mapped[list["Facility"]] = relationship(
        "Facility",
        secondary="experiment_to_facility_table",
        back_populates="experiments",
        lazy="selectin",
        info=dto_field("read-only")
    )

    experiment_type_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("vocabulary_table.id"))
    experiment_type: Mapped[Optional["Vocabulary"]] = relationship(
        "Vocabulary",
        back_populates="experiment",
        lazy="selectin",
        info=dto_field("read-only")
    )

    study_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("study_table.id"))
    study: Mapped[Optional["Study"]] = relationship(
        "Study",
        back_populates="experiments",
        lazy="selectin",
        info=dto_field("read-only")
    )
