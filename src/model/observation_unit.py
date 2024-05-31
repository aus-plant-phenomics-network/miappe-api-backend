from uuid import UUID

from sqlalchemy import UUID as UUID_SQL
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column

from src.model import Base

__all__ = ("ObservationUnit",)


ob_unit_to_ob_unit_table = Table(
    "ob_unit_to_ob_unit_table",
    Base.metadata,
    Column("parent_id", UUID_SQL, ForeignKey("observation_unit_table.id"), primary_key=True),
    Column("child_id", UUID_SQL, ForeignKey("observation_unit_table.id"), primary_key=True),
)


class ObservationUnit(Base):
    __tablename__ = "observation_unit_table"
    location: Mapped[str | None]

    # Relationship
    study_id: Mapped[UUID | None] = mapped_column(ForeignKey("study_table.id"))
    # study: Mapped[Optional["Study"]] = relationship("Study", lazy="selectin", info=dto_field("read-only"))

    facility_id: Mapped[UUID | None] = mapped_column(ForeignKey("facility_table.id"))
    # facility: Mapped[Optional["Facility"]] = relationship(
    #     "Facility", back_populates="observation_units", lazy="selectin", info=dto_field("read-only")
    # )

    observation_unit_type_id: Mapped[UUID | None] = mapped_column(ForeignKey("vocabulary_table.id"))
    # observation_unit_type: Mapped[Optional["Vocabulary"]] = relationship(
    #     "Vocabulary", back_populates="observation_units", lazy="selectin", info=dto_field("read-only")
    # )

    biological_material_id: Mapped[UUID | None] = mapped_column(ForeignKey("variable_table.id"))
    # biological_material: Mapped[Optional["Variable"]] = relationship(
    #     "Variable",
    #     back_populates="observation_unit_biological_materials",
    #     lazy="selectin",
    #     info=dto_field("read-only"),
    #     foreign_keys=[biological_material_id],
    # )

    factor_id: Mapped[UUID | None] = mapped_column(ForeignKey("variable_table.id"))
    # factor: Mapped[Optional["Variable"]] = relationship(
    #     "Variable",
    #     back_populates="observation_unit_factors",
    #     lazy="selectin",
    #     info=dto_field("read-only"),
    #     foreign_keys=[factor_id],
    # )

    # event: Mapped[list["Event"]] = relationship(
    #     "Event", back_populates="observation_unit", lazy="selectin", info=dto_field("read-only")
    # )
    # sample: Mapped[list["Sample"]] = relationship(
    #     "Sample", back_populates="observation_unit", lazy="selectin", info=dto_field("read-only")
    # )

    # parents: Mapped[list["ObservationUnit"]] = relationship(
    #     "ObservationUnit",
    #     secondary="ob_unit_to_ob_unit_table",
    #     back_populates="children",
    #     lazy="selectin",
    #     info=dto_field("read-only"),
    #     primaryjoin="ObservationUnit.id == ob_unit_to_ob_unit_table.c.child_id",
    #     secondaryjoin="ObservationUnit.id == ob_unit_to_ob_unit_table.c.parent_id",
    # )

    # children: Mapped[list["ObservationUnit"]] = relationship(
    #     "ObservationUnit",
    #     secondary="ob_unit_to_ob_unit_table",
    #     back_populates="parents",
    #     lazy="selectin",
    #     info=dto_field("read-only"),
    #     secondaryjoin="ObservationUnit.id == ob_unit_to_ob_unit_table.c.child_id",
    #     primaryjoin="ObservationUnit.id == ob_unit_to_ob_unit_table.c.parent_id",
    # )
