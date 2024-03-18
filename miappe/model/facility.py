from typing import Optional, TYPE_CHECKING
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from miappe.model import Base

if TYPE_CHECKING:
    from miappe.model.vocabulary import Vocabulary


class Facility(Base):
    __tablename__ = "facility_table"

    facility_type_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("vocabulary_table.id"))
    address: Mapped[Optional[str]]
    city: Mapped[Optional[str]]
    region: Mapped[Optional[str]]
    country: Mapped[Optional[str]]
    postcode: Mapped[Optional[str]]
    latitude: Mapped[Optional[str]]
    longitude: Mapped[Optional[str]]
    altitude: Mapped[Optional[str]]

    # TODO: add insitution

    # TODO: add variable group table

    # Relationship
    facility_type: Mapped[Optional["Vocabulary"]] = relationship(
        "Vocabulary", back_populates="facility", lazy="selectin", info=dto_field("read-only")
    )
