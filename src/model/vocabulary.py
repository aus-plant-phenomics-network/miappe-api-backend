from typing import TYPE_CHECKING

from litestar.dto import dto_field
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.base import Base

__all__ = ("Vocabulary",)


if TYPE_CHECKING:
    from src.model.device import Device

    #     from src.model.event import Event
    #     from src.model.experiment import Experiment
    #     from src.model.facility import Facility
    from src.model.institution import Institution
    from src.model.method import Method

    #     from src.model.observation_unit import ObservationUnit
    #     from src.model.sample import Sample
    from src.model.unit import Unit


class Vocabulary(Base):
    __tablename__: str = "vocabulary_table"  # type: ignore[assignment]
    title: Mapped[str]
    # Todo: use the same terminologies as PHIS - extract, widening, narrowing?
    relationship_type: Mapped[str | None]

    external_reference: Mapped[str | None]

    # Todo: Make namespace a separate entity?
    namespace: Mapped[str | None] = mapped_column(server_default="APPN")

    # # Relationships
    device: Mapped[list["Device"]] = relationship(back_populates="device_type", lazy=None, info=dto_field("private"))
    method: Mapped[list["Method"]] = relationship(back_populates="method_type", lazy=None, info=dto_field("private"))
    unit: Mapped[list["Unit"]] = relationship(back_populates="unit_type", lazy=None, info=dto_field("private"))

    # event: Mapped[list["Event"]] = relationship(back_populates="event_type", lazy="selectin", info=dto_field("private"))
    # sample_plant_structural_development_stage: Mapped[list["Sample"]] = relationship(
    #     back_populates="plant_structural_development_stage",
    #     lazy="selectin",
    #     primaryjoin="Vocabulary.id == Sample.plant_structural_development_stage_id",
    #     info=dto_field("private"),
    # )
    # sample_plant_anatomical_entity: Mapped[list["Sample"]] = relationship(
    #     back_populates="plant_anatomical_entity",
    #     primaryjoin="Vocabulary.id == Sample.plant_anatomical_entity_id",
    #     lazy="selectin",
    #     info=dto_field("private"),
    # )
    # facility: Mapped[list["Facility"]] = relationship(
    #     back_populates="facility_type", lazy="selectin", info=dto_field("private")
    # )
    institution: Mapped[list["Institution"]] = relationship(
        back_populates="institution_type", lazy=None, info=dto_field("private")
    )
    # experiment: Mapped[list["Experiment"]] = relationship(
    #     back_populates="experiment_type", lazy="selectin", info=dto_field("private")
    # )
    # observation_units: Mapped[list["ObservationUnit"]] = relationship(
    #     "ObservationUnit", back_populates="observation_unit_type", lazy="selectin", info=dto_field("read-only")
    # )
