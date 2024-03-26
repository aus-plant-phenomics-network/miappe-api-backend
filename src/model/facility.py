from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model import Base

__all__ = ("Facility",)


if TYPE_CHECKING:
    from src.model.experiment import Experiment
    from src.model.institution import Institution
    from src.model.observation_unit import ObservationUnit
    from src.model.variable import Variable
    from src.model.vocabulary import Vocabulary

facility_variable_table = Table(
    "facility_variable_table",
    Base.metadata,
    Column("facility_id", UUID_SQL, ForeignKey("facility_table.id"), primary_key=True),
    Column("variable_id", UUID_SQL, ForeignKey("variable_table.id"), primary_key=True),
)


class Facility(Base):
    __tablename__ = "facility_table"  # type: ignore[assignment]

    address: Mapped[str | None]
    city: Mapped[str | None]
    region: Mapped[str | None]
    country: Mapped[str | None]
    postcode: Mapped[str | None]
    latitude: Mapped[str | None]
    longitude: Mapped[str | None]
    altitude: Mapped[str | None]

    # relationship
    institution_id: Mapped[UUID | None] = mapped_column(ForeignKey("institution_table.id"))
    institution: Mapped[Optional["Institution"]] = relationship(
        "Institution", back_populates="facilities", lazy="selectin", info=dto_field("read-only")
    )

    variables: Mapped[list["Variable"]] = relationship(
        "Variable",
        secondary="facility_variable_table",
        back_populates="facilities",
        lazy="selectin",
        info=dto_field("read-only"),
    )

    # Relationship
    facility_type_id: Mapped[UUID | None] = mapped_column(ForeignKey("vocabulary_table.id"))
    facility_type: Mapped[Optional["Vocabulary"]] = relationship(
        "Vocabulary", back_populates="facility", lazy="selectin", info=dto_field("read-only")
    )
    experiments: Mapped[list["Experiment"]] = relationship(
        "Experiment",
        secondary="experiment_to_facility_table",
        back_populates="facilities",
        lazy="selectin",
        info=dto_field("read-only"),
    )