from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, cast
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.base import Base, BaseDataclass, Serialisable

__all__ = ("Institution",)


if TYPE_CHECKING:
    from src.model.facility import Facility
    from src.model.staff import Staff
    from src.model.vocabulary import Vocabulary

institution_to_institution_table = Table(
    "institution_to_institution_table",
    Base.metadata,
    Column("child_id", UUID_SQL, ForeignKey("institution_table.id", ondelete="cascade"), primary_key=True),
    Column("parent_id", UUID_SQL, ForeignKey("institution_table.id", ondelete="cascade"), primary_key=True),
)


class Institution(Base):
    __tablename__ = "institution_table"
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    country: Mapped[str | None] = mapped_column(nullable=True)

    # Relationship
    institution_type_id: Mapped[UUID | None] = mapped_column(ForeignKey("vocabulary_table.id", ondelete="SET NULL"))
    institution_type: Mapped[Optional["Vocabulary"]] = relationship(
        back_populates="institution",
        lazy=None,
        info=dto_field("read-only"),
    )
    staffs: Mapped[list["Staff"]] = relationship(
        lazy=None,
        secondary="institution_staff_table",
        info=dto_field("read-only"),
        back_populates="institutions",
    )
    facilities: Mapped[list["Facility"]] = relationship(
        back_populates="institution",
        lazy=None,
        info=dto_field("read-only"),
    )

    children: Mapped[list["Institution"]] = relationship(
        secondary="institution_to_institution_table",
        back_populates="parents",
        lazy=None,
        info=dto_field("read-only"),
        primaryjoin="Institution.id == institution_to_institution_table.c.parent_id",
        secondaryjoin="Institution.id == institution_to_institution_table.c.child_id",
        cascade="all, delete",
    )

    parents: Mapped[list["Institution"]] = relationship(
        secondary="institution_to_institution_table",
        back_populates="children",
        lazy=None,
        info=dto_field("read-only"),
        primaryjoin="Institution.id == institution_to_institution_table.c.child_id",
        secondaryjoin="Institution.id == institution_to_institution_table.c.parent_id",
        cascade="all, delete",
    )


@dataclass(kw_only=True)
class InstitutionDataclass(BaseDataclass):
    name: str
    country: str | None = field(default=None)
    institution_type_id: UUID | None = field(default=None)
    parent_id: list[UUID] = field(default_factory=list[UUID])

    @classmethod
    def from_orm(cls, data: Serialisable) -> "InstitutionDataclass":
        data = cast(Institution, data)
        data_dict = data.to_dict()
        if len(data.parents) > 0:
            data_dict["parent_id"] = [item.id for item in data.parents]
        return cls(**data_dict)
