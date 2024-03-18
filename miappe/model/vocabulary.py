from typing import TYPE_CHECKING, Optional

from litestar.dto import dto_field
from sqlalchemy.orm import Mapped, mapped_column, relationship

from miappe.model.base import Base

if TYPE_CHECKING:
    from miappe.model.device import Device
    from miappe.model.method import Method
    from miappe.model.unit import Unit
    from miappe.model.variable import Variable
    from miappe.model.event import Event
    from miappe.model.sample import Sample
    from miappe.model.facility import Facility
    from miappe.model.institution import Institution
    from miappe.model.experiment import Experiment
    from miappe.model.observation_unit import ObservationUnit


class Vocabulary(Base):
    __tablename__: str = "vocabulary_table"  # type: ignore

    external_reference: Mapped[Optional[str]]

    # Todo: Make namespace a separate entity?
    namespace: Mapped[Optional[str]] = mapped_column(server_default="APPN")

    # Todo: use the same terminologies as PHIS - extract, widening, narrowing?
    relationship_type: Mapped[Optional[str]]

    # Relationships
    device: Mapped[list["Device"]] = relationship(
        back_populates="device_type", lazy="selectin", info=dto_field("private")
    )
    method: Mapped[list["Method"]] = relationship(
        back_populates="method_type", lazy="selectin", info=dto_field("private")
    )
    unit: Mapped[list["Unit"]] = relationship(
        back_populates="unit_type", lazy="selectin", info=dto_field("private")
    )
    variable: Mapped[list["Variable"]] = relationship(
        back_populates="variable_type", lazy="selectin", info=dto_field("private")
    )
    event: Mapped[list["Event"]] = relationship(
        back_populates="event_type", lazy="selectin", info=dto_field("private")
    )
    sample_plant_structural_development_stage: Mapped[list["Sample"]] = relationship(
        back_populates="plant_structural_development_stage",
        lazy="selectin",
        primaryjoin="Vocabulary.id == Sample.plant_structural_development_stage_id",
        info=dto_field("private")
    )
    sample_plant_anatomical_entity: Mapped[list["Sample"]] = relationship(
        back_populates="plant_anatomical_entity",
        primaryjoin="Vocabulary.id == Sample.plant_anatomical_entity_id",
        lazy="selectin",
        info=dto_field("private"),
    )
    facility: Mapped[list["Facility"]] = relationship(
        back_populates="facility_type", lazy="selectin", info=dto_field("private")
    )
    institution: Mapped[list["Institution"]] = relationship(
        back_populates="institution_type", lazy="selectin", info=dto_field("private")
    )
    experiment: Mapped[list["Experiment"]] = relationship(
        back_populates="experiment_type", lazy="selectin", info=dto_field("private")
    )
    observation_units: Mapped[list["ObservationUnit"]] = relationship(
        "ObservationUnit",
        back_populates="observation_unit_type",
        lazy="selectin",
        info=dto_field("read-only")
    )