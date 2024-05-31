from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, cast
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.base import Base, BaseDataclass, Serialisable

if TYPE_CHECKING:
    from src.model.biological_material import BiologicalMaterial
    from src.model.event import Event
    from src.model.experimental_factor import ExperimentalFactor
    from src.model.facility import Facility
    from src.model.sample import Sample
    from src.model.study import Study
    from src.model.vocabulary import Vocabulary

__all__ = ("ObservationUnit",)


ob_unit_to_ob_unit_table = Table(
    "ob_unit_to_ob_unit_table",
    Base.metadata,
    Column("parent_id", UUID_SQL, ForeignKey("observation_unit_table.id"), primary_key=True),
    Column("child_id", UUID_SQL, ForeignKey("observation_unit_table.id"), primary_key=True),
)


class ObservationUnit(Base):
    __tablename__ = "observation_unit_table"
    title: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str | None]
    # Relationship
    study_id: Mapped[UUID | None] = mapped_column(ForeignKey("study_table.id"))
    study: Mapped[Optional["Study"]] = relationship(
        "Study",
        lazy=None,
        info=dto_field("read-only"),
        back_populates="observation_unit",
    )

    facility_id: Mapped[UUID | None] = mapped_column(ForeignKey("facility_table.id"))
    facility: Mapped[Optional["Facility"]] = relationship(
        "Facility",
        back_populates="observation_unit",
        lazy=None,
        info=dto_field("read-only"),
    )

    observation_unit_type_id: Mapped[UUID | None] = mapped_column(ForeignKey("vocabulary_table.id"))
    observation_unit_type: Mapped[Optional["Vocabulary"]] = relationship(
        "Vocabulary",
        back_populates="observation_unit",
        lazy=None,
        info=dto_field("read-only"),
    )

    biological_material_id: Mapped[UUID | None] = mapped_column(ForeignKey("biological_material_table.id"))
    biological_material: Mapped[Optional["BiologicalMaterial"]] = relationship(
        "BiologicalMaterial",
        back_populates="observation_unit",
        lazy=None,
        info=dto_field("read-only"),
    )

    factor_id: Mapped[UUID | None] = mapped_column(ForeignKey("experimental_factor_table.id"))
    factor: Mapped[Optional["ExperimentalFactor"]] = relationship(
        "ExperimentalFactor",
        back_populates="observation_unit",
        lazy=None,
        info=dto_field("read-only"),
    )
    factor_value: Mapped[str | None]

    event: Mapped[list["Event"]] = relationship(
        "Event",
        back_populates="observation_unit",
        lazy=None,
        info=dto_field("read-only"),
    )
    sample: Mapped[list["Sample"]] = relationship(
        "Sample",
        back_populates="observation_unit",
        lazy=None,
        info=dto_field("read-only"),
    )

    parents: Mapped[list["ObservationUnit"]] = relationship(
        "ObservationUnit",
        secondary="ob_unit_to_ob_unit_table",
        back_populates="children",
        lazy=None,
        info=dto_field("read-only"),
        primaryjoin="ObservationUnit.id == ob_unit_to_ob_unit_table.c.child_id",
        secondaryjoin="ObservationUnit.id == ob_unit_to_ob_unit_table.c.parent_id",
    )

    children: Mapped[list["ObservationUnit"]] = relationship(
        "ObservationUnit",
        secondary="ob_unit_to_ob_unit_table",
        back_populates="parents",
        lazy=None,
        info=dto_field("read-only"),
        secondaryjoin="ObservationUnit.id == ob_unit_to_ob_unit_table.c.child_id",
        primaryjoin="ObservationUnit.id == ob_unit_to_ob_unit_table.c.parent_id",
    )


@dataclass(kw_only=True)
class ObservationUnitDataclass(BaseDataclass):
    title: str
    location: str | None = field(default=None)
    study_id: UUID | None = field(default=None)
    facility_id: UUID | None = field(default=None)
    observation_unit_type_id: UUID | None = field(default=None)
    biological_material_id: UUID | None = field(default=None)
    factor_id: UUID | None = field(default=None)
    factor_value: str | None = field(default=None)
    parent_id: list[UUID] = field(default_factory=list[UUID])

    @classmethod
    def from_orm(cls, data: Serialisable) -> "ObservationUnitDataclass":
        data = cast(ObservationUnit, data)
        data_dict = data.to_dict()
        if len(data.parents) > 0:
            data_dict["parent_id"] = [item.id for item in data.parents]
        return cls(**data_dict)
