import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model import Base

if TYPE_CHECKING:
    from src.model.observation_unit import ObservationUnit
    from src.model.vocabulary import Vocabulary

__all__ = ("Sample",)


class Sample(Base):
    __tablename__ = "sample_table"

    observation_unit_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("observation_unit_table.id", ondelete="SET NULL")
    )
    plant_structural_development_stage_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("vocabulary_table.id", ondelete="SET NULL")
    )
    plant_anatomical_entity_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("vocabulary_table.id", ondelete="SET NULL")
    )
    collection_date: Mapped[datetime.datetime | None]

    # Relationship
    observation_unit: Mapped[Optional["ObservationUnit"]] = relationship(
        back_populates="samples",
        lazy=None,
        info=dto_field("read-only"),
    )
    plant_structural_development_stage: Mapped[Optional["Vocabulary"]] = relationship(
        foreign_keys=[plant_structural_development_stage_id],
        back_populates="sample_plant_structural_development_stage",
        lazy=None,
        info=dto_field("read-only"),
    )
    plant_anatomical_entity: Mapped[Optional["Vocabulary"]] = relationship(
        foreign_keys=[plant_anatomical_entity_id],
        back_populates="sample_plant_anatomical_entity",
        lazy=None,
        info=dto_field("read-only"),
    )
