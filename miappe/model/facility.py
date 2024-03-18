from typing import Optional, TYPE_CHECKING
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from miappe.model import Base

if TYPE_CHECKING:
    from miappe.model.vocabulary import Vocabulary
    from miappe.model.experiment import Experiment
    from miappe.model.institution import Institution
    from miappe.model.variable import Variable
    from miappe.model.observation_unit import ObservationUnit

facility_variable_table = Table(
    "facility_variable_table",
    Base.metadata,
    Column("facility_id", UUID_SQL, ForeignKey("facility_table.id"), primary_key=True),
    Column("variable_id", UUID_SQL, ForeignKey("variable_table.id"), primary_key=True)
)


class Facility(Base):
    __tablename__ = "facility_table"

    address: Mapped[Optional[str]]
    city: Mapped[Optional[str]]
    region: Mapped[Optional[str]]
    country: Mapped[Optional[str]]
    postcode: Mapped[Optional[str]]
    latitude: Mapped[Optional[str]]
    longitude: Mapped[Optional[str]]
    altitude: Mapped[Optional[str]]

    # relationship
    institution_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("institution_table.id"))
    institution: Mapped[Optional["Institution"]] = relationship(
        "Institution", back_populates="facilities", lazy="selectin", info=dto_field("read-only")
    )

    variables: Mapped[list["Variable"]] = relationship("Variable",
                                                       secondary="facility_variable_table",
                                                       back_populates="facilities", lazy="selectin",
                                                       info=dto_field("read-only"))

    # Relationship
    facility_type_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("vocabulary_table.id"))
    facility_type: Mapped[Optional["Vocabulary"]] = relationship(
        "Vocabulary",
        back_populates="facility", lazy="selectin", info=dto_field("read-only")
    )
    experiments: Mapped[list["Experiment"]] = relationship(
        "Experiment", secondary="experiment_to_facility_table",
        back_populates="facilities", lazy="selectin", info=dto_field("read-only")
    )
    observation_units: Mapped[list["ObservationUnit"]] = relationship(
        "ObservationUnit",
        back_populates="facility",
        lazy="selectin",
        info=dto_field("read-only")
    )
