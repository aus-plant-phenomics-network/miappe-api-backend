from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model import Base

__all__ = ("Staff",)


if TYPE_CHECKING:
    from src.model.institution import Institution


class Staff(Base):
    __tablename__ = "staff_table"  # type: ignore[assignment]

    email: Mapped[str | None]
    phone: Mapped[str | None]
    orcid: Mapped[str | None]
    role: Mapped[str | None]

    # Relationship
    institution_id: Mapped[UUID | None] = mapped_column(ForeignKey("institution_table.id"))
    affiliation: Mapped[Optional["Institution"]] = relationship(
        "Institution", back_populates="staffs", lazy="selectin", info=dto_field("read-only")
    )
