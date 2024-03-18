from typing import Optional, TYPE_CHECKING
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from miappe.model import Base

if TYPE_CHECKING:
    from miappe.model.institution import Institution


class Staff(Base):
    __tablename__ = "staff_table"

    name: Mapped[str]
    email: Mapped[Optional[str]]
    phone: Mapped[Optional[str]]
    orcid: Mapped[Optional[str]]
    institution_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("institution_table.id"))
    role: Mapped[Optional[str]]

    # Relationship
    affiliation: Mapped[Optional["Institution"]] = relationship(
        "Institution",
        back_populates="staff",
        lazy="selectin",
        info=dto_field("read-only")
    )
