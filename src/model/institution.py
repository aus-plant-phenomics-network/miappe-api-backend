from typing import Optional, TYPE_CHECKING
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model import Base

if TYPE_CHECKING:
    from src.model.vocabulary import Vocabulary
    from src.model.staff import Staff
    from src.model.facility import Facility

institution_to_institution_table = Table(
    "institution_to_institution_table",
    Base.metadata,
    Column("child_id", UUID_SQL, ForeignKey("institution_table.id"), primary_key=True),
    Column("parent_id", UUID_SQL, ForeignKey("institution_table.id"), primary_key=True),
)


class Institution(Base):
    __tablename__ = "institution_table"  # type: ignore[assignment]

    # Relationship
    institution_type_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("vocabulary_table.id"))
    institution_type: Mapped[Optional["Vocabulary"]] = relationship(
        "Vocabulary", back_populates="institution", lazy="selectin", info=dto_field("read-only")
    )
    staffs: Mapped[list["Staff"]] = relationship("Staff", back_populates="affiliation", lazy="selectin",
                                                 info=dto_field("read-only"))
    facilities: Mapped[list["Facility"]] = relationship(
        "Facility", back_populates="institution", lazy="selectin", info=dto_field("read-only"))

    children: Mapped[list["Institution"]] = relationship(
        "Institution",
        secondary="institution_to_institution_table",
        back_populates="parents",
        lazy="selectin",
        info=dto_field("read-only"),
        primaryjoin="Institution.id == institution_to_institution_table.c.parent_id",
        secondaryjoin="Institution.id == institution_to_institution_table.c.child_id",
    )

    parents: Mapped[list["Institution"]] = relationship(
        "Institution",
        secondary="institution_to_institution_table",
        back_populates="children",
        lazy="selectin",
        info=dto_field("read-only"),
        primaryjoin="Institution.id == institution_to_institution_table.c.child_id",
        secondaryjoin="Institution.id == institution_to_institution_table.c.parent_id",
    )
