# from typing import TYPE_CHECKING, Optional
# from uuid import UUID

# from litestar.dto import dto_field
# from sqlalchemy import UUID as UUID_SQL
# from sqlalchemy import Column, ForeignKey, Table
# from sqlalchemy.orm import Mapped, mapped_column, relationship

# from src.model.base import Base

# __all__ = ("Variable",)


# if TYPE_CHECKING:
#     from src.model.biological_material import BiologicalMaterial
#     from src.model.device import Device
#     from src.model.environment import Environment
#     from src.model.facility import Facility
#     from src.model.observation_unit import ObservationUnit
#     from src.model.study import Study
#     from src.model.vocabulary import Vocabulary

# study_variable_table = Table(
#     "study_variable_table",
#     Base.metadata,
#     Column("study_id", UUID_SQL, ForeignKey("study_table.id"), primary_key=True),
#     Column("variable_id", UUID_SQL, ForeignKey("variable_table.id"), primary_key=True),
# )


# class Variable(Base):
#     __tablename__: str = "variable_table"  # type: ignore[assignment]

#     time_interval: Mapped[str | None]
#     sample_interval: Mapped[str | None]

#     # Relationships:
#     variable_type_id: Mapped[UUID | None] = mapped_column(ForeignKey("vocabulary_table.id"))
#     variable_type: Mapped[Optional["Vocabulary"]] = relationship(
#         back_populates="variable", lazy="selectin", info=dto_field("read-only")
#     )

#     device_id: Mapped[UUID | None] = mapped_column(ForeignKey("device_table.id"))
#     device: Mapped[Optional["Device"]] = relationship(lazy="selectin", info=dto_field("read-only"))

#     # Sub-variable relationship
#     biological_material: Mapped[Optional["BiologicalMaterial"]] = relationship(
#         back_populates="variable", lazy="selectin", info=dto_field("read-only")
#     )
#     environment: Mapped[Optional["Environment"]] = relationship(
#         back_populates="variable", lazy="selectin", info=dto_field("read-only")
#     )

#     # Variable to study relationship
#     studies: Mapped[list["Study"]] = relationship(
#         "Study",
#         secondary="study_variable_table",
#         back_populates="variables",
#         lazy="selectin",
#         info=dto_field("read-only"),
#     )

#     facilities: Mapped[list["Facility"]] = relationship(
#         "Facility",
#         secondary="facility_variable_table",
#         back_populates="variables",
#         lazy="selectin",
#         info=dto_field("read-only"),
#     )

#     observation_unit_biological_materials: Mapped[list["ObservationUnit"]] = relationship(
#         "ObservationUnit",
#         back_populates="biological_material",
#         lazy="selectin",
#         info=dto_field("read-only"),
#         primaryjoin="Variable.id== ObservationUnit.biological_material_id",
#     )

#     observation_unit_factors: Mapped[list["ObservationUnit"]] = relationship(
#         "ObservationUnit",
#         back_populates="factor",
#         lazy="selectin",
#         info=dto_field("read-only"),
#         primaryjoin="Variable.id == ObservationUnit.factor_id",
#     )
