from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model import Base

__all__ = ("Facility",)


if TYPE_CHECKING:
    from src.model.experiment import Experiment
    from src.model.institution import Institution
    from src.model.observation_unit import ObservationUnit
    from src.model.vocabulary import Vocabulary


class Facility(Base):
    __tablename__ = "facility_table"
    name: Mapped[str]
    description: Mapped[str | None]
    address: Mapped[str | None]
    city: Mapped[str | None]
    region: Mapped[str | None]
    country: Mapped[str | None]
    postcode: Mapped[str | None]
    latitude: Mapped[str | None]
    longitude: Mapped[str | None]
    altitude: Mapped[str | None]

    # relationship
    institution_id: Mapped[UUID | None] = mapped_column(ForeignKey("institution_table.id", ondelete="SET NULL"))
    institution: Mapped[Optional["Institution"]] = relationship(
        back_populates="facilities",
        lazy=None,
        info=dto_field("read-only"),
    )

    facility_type_id: Mapped[UUID | None] = mapped_column(ForeignKey("vocabulary_table.id", ondelete="SET NULL"))
    facility_type: Mapped[Optional["Vocabulary"]] = relationship(
        back_populates="facility",
        lazy=None,
        info=dto_field("read-only"),
    )
    experiments: Mapped[list["Experiment"]] = relationship(
        secondary="experiment_to_facility_table",
        back_populates="facilities",
        lazy=None,
        info=dto_field("read-only"),
    )
    observation_units: Mapped[list["ObservationUnit"]] = relationship(
        back_populates="facility",
        lazy=None,
        info=dto_field("read-only"),
    )
