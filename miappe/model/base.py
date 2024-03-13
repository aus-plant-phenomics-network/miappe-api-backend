from uuid import uuid4, UUID

from advanced_alchemy.base import AuditColumns, CommonTableAttributes
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


class Base(AuditColumns, CommonTableAttributes, DeclarativeBase):
    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"id: {self.id}, name: {self.name}, description: {self.description}"