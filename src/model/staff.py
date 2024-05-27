from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, relationship

from src.model.base import Base, BaseDataclass

if TYPE_CHECKING:
    from src.model.institution import Institution

__all__ = ("Staff", "StaffDataclass")

institution_staff_table = Table(
    "institution_staff_table",
    Base.metadata,
    Column("institution_id", UUID_SQL, ForeignKey("institution_table.id"), primary_key=True),
    Column("staff_id", UUID_SQL, ForeignKey("staff_table.id"), primary_key=True),
)


class Staff(Base):
    __tablename__ = "staff_table"  # type: ignore[assignment]

    email: Mapped[str | None]
    phone: Mapped[str | None]
    orcid: Mapped[str | None]
    role: Mapped[str | None]

    # Relationship
    institutions: Mapped[list["Institution"]] = relationship(
        "Institution",
        secondary="institution_staff_table",
        back_populates="staffs",
        lazy=None,
        info=dto_field("read-only"),
    )


@dataclass
class StaffDataclass(BaseDataclass):
    email: str | None = field(default=None)
    phone: str | None = field(default=None)
    orcid: str | None = field(default=None)
    role: str | None = field(default=None)
    institution_id: list[UUID] = field(default_factory=list[UUID])

    @classmethod
    def from_orm(cls, data: Staff) -> "StaffDataclass":  # type: ignore[override]
        data_dict = data.to_dict()
        if len(data.institutions) > 0:
            data_dict["institution_id"] = [item.id for item in data.institutions]
        return cls(**data_dict)
