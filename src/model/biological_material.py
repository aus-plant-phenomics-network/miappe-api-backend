from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.base import BaseDataclass
from src.model.variable import Variable

__all__ = ("BiologicalMaterial",)


if TYPE_CHECKING:
    from src.model.method import Method
    from src.model.vocabulary import Vocabulary


class BiologicalMaterial(Variable):
    __tablename__: str = "biological_material_table"  # type: ignore[assignment]
    __mapper_args__ = {"polymorphic_identity": "biological_material"}

    id: Mapped[UUID] = mapped_column(ForeignKey("variable_table.id"), primary_key=True, info=dto_field("read-only"))
    title: Mapped[str] = mapped_column(nullable=False)
    organism_id: Mapped[UUID] = mapped_column(ForeignKey("vocabulary_table.id", ondelete="SET NULL"))
    organism: Mapped["Vocabulary"] = relationship(
        "Vocabulary", lazy=None, info=dto_field("read-only"), back_populates="organism"
    )
    genus: Mapped[str | None]
    species: Mapped[str | None]
    infraspecific_name: Mapped[str | None]

    biological_material_latitude: Mapped[str | None]
    biological_material_longitude: Mapped[str | None]
    biological_material_altitude: Mapped[str | None]
    biological_material_coordinates_uncertainty: Mapped[str | None]

    material_source_id: Mapped[str | None]
    material_source_doi: Mapped[str | None]
    material_source_latitude: Mapped[str | None]
    material_source_longitude: Mapped[str | None]
    material_source_altitude: Mapped[str | None]
    material_source_coordinates_uncertainty: Mapped[str | None]
    material_source_description: Mapped[str | None]

    # Relationship
    preprocessing_method_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("method_table.id"),
    )
    preprocessing_method: Mapped[Optional["Method"]] = relationship(
        back_populates="biological_material",
        lazy=None,
        info=dto_field("read-only"),
    )


@dataclass(kw_only=True)
class BiologicalMaterialDataclass(BaseDataclass):
    title: str
    organism_id: UUID | None = field(default=None)
    genus: str | None = field(default=None)
    species: str | None = field(default=None)
    infraspecific_name: str | None = field(default=None)
    biological_material_latitude: str | None = field(default=None)
    biological_material_longitude: str | None = field(default=None)
    biological_material_altitude: str | None = field(default=None)
    biological_material_coordinates_uncertainty: str | None = field(default=None)
    material_source_id: str | None = field(default=None)
    material_source_doi: str | None = field(default=None)
    material_source_latitude: str | None = field(default=None)
    material_source_longitude: str | None = field(default=None)
    material_source_altitude: str | None = field(default=None)
    material_source_coordinates_uncertainty: str | None = field(default=None)
    material_source_description: str | None = field(default=None)
    preprocessing_method_id: UUID | None = field(default=None)
