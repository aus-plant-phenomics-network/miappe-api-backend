from typing import Optional, TYPE_CHECKING
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from miappe.model import Base

if TYPE_CHECKING:
    from miappe.model.vocabulary import Vocabulary
    from miappe.model.staff import Staff


class Institution(Base):
    __tablename__ = "institution_table"

    institution_type_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("vocabulary_table.id"))

    # Relationship
    institution_type: Mapped[Optional["Vocabulary"]] = relationship(
        "Vocabulary", back_populates="institution", lazy="selectin", info=dto_field("read-only")
    )
    staff: Mapped[list["Staff"]] = relationship("Staff", back_populates="affiliation", lazy="selectin",
                                                info=dto_field("read-only"))
