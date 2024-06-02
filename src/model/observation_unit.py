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
    Column("parent_id", UUID_SQL, ForeignKey("observation_unit_table.id", ondelete="cascade"), primary_key=True),
    Column("child_id", UUID_SQL, ForeignKey("observation_unit_table.id", ondelete="cascade"), primary_key=True),
)

ob_unit_to_study_table = Table(
    "ob_unit_to_study_table",
    Base.metadata,
    Column(
        "observation_unit_id", UUID_SQL, ForeignKey("observation_unit_table.id", ondelete="cascade"), primary_key=True
    ),
    Column("study_id", UUID_SQL, ForeignKey("study_table.id", ondelete="cascade"), primary_key=True),
)

ob_unit_to_exp_factor_table = Table(
    "ob_unit_to_exp_factor_table",
    Base.metadata,
    Column(
        "observation_unit_id", UUID_SQL, ForeignKey("observation_unit_table.id", ondelete="cascade"), primary_key=True
    ),
    Column(
        "experimental_factor_id",
        UUID_SQL,
        ForeignKey("experimental_factor_table.id", ondelete="cascade"),
        primary_key=True,
    ),
)


class ObservationUnit(Base):
    __tablename__ = "observation_unit_table"
    title: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str | None]
    # Relationship
    studies: Mapped[list["Study"]] = relationship(
        secondary="ob_unit_to_study_table",
        lazy=None,
        info=dto_field("read-only"),
        back_populates="observation_unit",
    )

    facility_id: Mapped[UUID | None] = mapped_column(ForeignKey("facility_table.id", ondelete="SET NULL"))
    facility: Mapped[Optional["Facility"]] = relationship(
        back_populates="observation_units",
        lazy=None,
        info=dto_field("read-only"),
    )

    observation_unit_type_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("vocabulary_table.id", ondelete="SET NULL")
    )
    observation_unit_type: Mapped[Optional["Vocabulary"]] = relationship(
        back_populates="observation_unit",
        lazy=None,
        info=dto_field("read-only"),
    )

    biological_material_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("biological_material_table.id", ondelete="SET NULL")
    )
    biological_material: Mapped[Optional["BiologicalMaterial"]] = relationship(
        back_populates="observation_units",
        lazy=None,
        info=dto_field("read-only"),
    )

    experimental_factors: Mapped[list["ExperimentalFactor"]] = relationship(
        secondary="ob_unit_to_exp_factor_table",
        back_populates="observation_units",
        lazy=None,
        info=dto_field("read-only"),
    )

    events: Mapped[list["Event"]] = relationship(
        secondary="event_to_ob_unit_table",
        back_populates="observation_units",
        lazy=None,
        info=dto_field("read-only"),
    )
    samples: Mapped[list["Sample"]] = relationship(
        back_populates="observation_unit",
        lazy=None,
        info=dto_field("read-only"),
    )

    parents: Mapped[list["ObservationUnit"]] = relationship(
        secondary="ob_unit_to_ob_unit_table",
        back_populates="children",
        lazy=None,
        info=dto_field("read-only"),
        primaryjoin="ObservationUnit.id == ob_unit_to_ob_unit_table.c.child_id",
        secondaryjoin="ObservationUnit.id == ob_unit_to_ob_unit_table.c.parent_id",
    )

    children: Mapped[list["ObservationUnit"]] = relationship(
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
    facility_id: UUID | None = field(default=None)
    observation_unit_type_id: UUID | None = field(default=None)
    biological_material_id: UUID | None = field(default=None)
    experimental_factor_id: list[UUID] = field(default_factory=list[UUID])
    study_id: list[UUID] = field(default_factory=list[UUID])
    parent_id: list[UUID] = field(default_factory=list[UUID])

    @classmethod
    def from_orm(cls, data: Serialisable) -> "ObservationUnitDataclass":
        data = cast(ObservationUnit, data)
        data_dict = data.to_dict()
        if len(data.experimental_factors) > 0:
            data_dict["experimental_factor_id"] = [item.id for item in data.experimental_factors]
        if len(data.parents) > 0:
            data_dict["parent_id"] = [item.id for item in data.parents]
        if len(data.studies) > 0:
            data_dict["study_id"] = [item.id for item in data.studies]
        return cls(**data_dict)
