from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model import Base

__all__ = ("Institution",)


if TYPE_CHECKING:
    # from src.model.facility import Facility
    from src.model.staff import Staff
    from src.model.vocabulary import Vocabulary

institution_to_institution_table = Table(
    "institution_to_institution_table",
    Base.metadata,
    Column("child_id", UUID_SQL, ForeignKey("institution_table.id", ondelete="cascade"), primary_key=True),
    Column("parent_id", UUID_SQL, ForeignKey("institution_table.id", ondelete="cascade"), primary_key=True),
)


class Institution(Base):
    __tablename__ = "institution_table"  # type: ignore[assignment]

    # Relationship
    institution_type_id: Mapped[UUID | None] = mapped_column(ForeignKey("vocabulary_table.id", ondelete="SET NULL"))
    institution_type: Mapped[Optional["Vocabulary"]] = relationship(
        "Vocabulary", back_populates="institution", lazy="selectin", info=dto_field("read-only")
    )
    staffs: Mapped[list["Staff"]] = relationship("Staff", lazy=None, info=dto_field("read-only"))
    # facilities: Mapped[list["Facility"]] = relationship(
    #     "Facility", back_populates="institution", lazy="selectin", info=dto_field("read-only")
    # )

    children: Mapped[list["Institution"]] = relationship(
        "Institution",
        secondary="institution_to_institution_table",
        back_populates="parents",
        lazy=None,
        info=dto_field("read-only"),
        primaryjoin="Institution.id == institution_to_institution_table.c.parent_id",
        secondaryjoin="Institution.id == institution_to_institution_table.c.child_id",
        cascade="all, delete",
    )

    parents: Mapped[list["Institution"]] = relationship(
        "Institution",
        secondary="institution_to_institution_table",
        back_populates="children",
        lazy=None,
        info=dto_field("read-only"),
        primaryjoin="Institution.id == institution_to_institution_table.c.child_id",
        secondaryjoin="Institution.id == institution_to_institution_table.c.parent_id",
        cascade="all, delete",
    )
