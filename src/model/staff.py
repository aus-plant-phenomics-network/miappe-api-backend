from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.model import Base

__all__ = ("Staff",)


class Staff(Base):
    __tablename__ = "staff_table"  # type: ignore[assignment]

    email: Mapped[str | None]
    phone: Mapped[str | None]
    orcid: Mapped[str | None]
    role: Mapped[str | None]

    # Relationship
    institution_id: Mapped[UUID | None] = mapped_column(ForeignKey("institution_table.id", ondelete="SET NULL"))
