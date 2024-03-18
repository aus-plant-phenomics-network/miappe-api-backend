from typing import Optional, TYPE_CHECKING

from litestar.dto import dto_field
from sqlalchemy.orm import Mapped, relationship

from miappe.model import Base

if TYPE_CHECKING:
    from miappe.model.event import Event
    from miappe.model.sample import Sample


class ObservationUnit(Base):
    __tablename__ = "observation_unit_table"
    location: Mapped[Optional[str]]

    # TODO: add study and facility
    event: Mapped[list["Event"]] = relationship(
        "Event",
        back_populates="observation_unit",
        lazy="selectin",
        info=dto_field("read-only")
    )
    sample: Mapped[list["Sample"]] = relationship(
        "Sample",
        back_populates="observation_unit",
        lazy="selectin",
        info=dto_field("read-only")
    )
