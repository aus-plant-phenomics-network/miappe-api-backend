import datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from miappe.model import Base

if TYPE_CHECKING:
    from miappe.model.observation_unit import ObservationUnit
    from miappe.model.vocabulary import Vocabulary


class Sample(Base):
    __tablename__ = "sample_table"

    observation_unit_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("observation_unit_table.id"))
    plant_structural_development_stage_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("vocabulary_table.id"))
    plant_anatomical_entity_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("vocabulary_table.id"))
    collection_date: Mapped[Optional[datetime.datetime]]

    # Relationship
    observation_unit: Mapped[Optional["ObservationUnit"]] = relationship(
        "ObservationUnit",
        back_populates="sample",
        lazy="selectin",
        info=dto_field("read-only")
    )
    plant_structural_development_stage: Mapped[Optional["Vocabulary"]] = relationship(
        "Vocabulary",
        foreign_keys=[plant_structural_development_stage_id],
        back_populates="sample_plant_structural_development_stage",
        lazy="selectin",
        info=dto_field("read-only"),
    )
    plant_anatomical_entity: Mapped[Optional["Vocabulary"]] = relationship(
        "Vocabulary",
        foreign_keys=[plant_anatomical_entity_id],
        back_populates="sample_plant_anatomical_entity",
        lazy="selectin",
        info=dto_field("read-only"),
    )
