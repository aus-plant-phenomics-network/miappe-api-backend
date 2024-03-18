from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from miappe.model.base import Base

if TYPE_CHECKING:
    from miappe.model.biological_material import BiologicalMaterial
    from miappe.model.vocabulary import Vocabulary
    from miappe.model.environment import Environment
    from miappe.model.device import Device
    from miappe.model.study import Study

study_variable_table = Table(
    "study_variable_table",
    Base.metadata,
    Column("study_id", UUID_SQL, ForeignKey("study_table.id"), primary_key=True),
    Column("variable_id", UUID_SQL, ForeignKey("variable_table.id"), primary_key=True)
)


class Variable(Base):
    __tablename__: str = "variable_table"  # type: ignore

    time_interval: Mapped[Optional[str]]
    sample_interval: Mapped[Optional[str]]

    # Relationships:
    variable_type_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("vocabulary_table.id")
    )
    variable_type: Mapped[Optional["Vocabulary"]] = relationship(
        back_populates="variable", lazy="selectin", info=dto_field("read-only")
    )

    device_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("device_table.id"))
    device: Mapped[Optional["Device"]] = relationship(
        back_populates="variable", lazy="selectin", info=dto_field("read-only")
    )

    # Sub-variable relationship
    biological_material: Mapped[Optional["BiologicalMaterial"]] = relationship(
        back_populates="variable", lazy="selectin", info=dto_field("read-only")
    )
    environment: Mapped[Optional["Environment"]] = relationship(back_populates="variable", lazy="selectin",
                                                                info=dto_field("read-only"))

    # Variable to study relationship
    study: Mapped[list["Study"]] = relationship(
        "Study",
        secondary=study_variable_table,
        back_populates="variable",
        lazy="selectin",
        info=dto_field("read-only")
    )
