from typing import Optional, TYPE_CHECKING
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model import Base

if TYPE_CHECKING:
    from src.model.institution import Institution


class Staff(Base):
    __tablename__ = "staff_table"  # type: ignore[assignment]

    email: Mapped[Optional[str]]
    phone: Mapped[Optional[str]]
    orcid: Mapped[Optional[str]]
    role: Mapped[Optional[str]]

    # Relationship
    institution_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("institution_table.id"))
    affiliation: Mapped[Optional["Institution"]] = relationship(
        "Institution",
        back_populates="staffs",
        lazy="selectin",
        info=dto_field("read-only")
    )
