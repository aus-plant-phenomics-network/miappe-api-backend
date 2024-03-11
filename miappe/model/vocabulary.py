from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy.orm import mapped_column, Mapped, relationship
from miappe.model.base import Base


class Vocabulary(Base):
    __tablename__ = "vocabulary_table"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    external_reference: Mapped[Optional[str]]
    symbol: Mapped[Optional[str]]
    namespace: Mapped[Optional[str]] = mapped_column(default="APPN")  # Todo: Make namespace a separate entity?
    relationship_type: Mapped[Optional[str]]  # Todo: use the same terminologies as PHIS - extract, widening, narrowing?

    # Defining relationship
    device: Mapped["Device"] = relationship(back_populates="device_type")
