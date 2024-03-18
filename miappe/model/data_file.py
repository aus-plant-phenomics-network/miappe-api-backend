from typing import Optional, TYPE_CHECKING
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from miappe.model import Base

if TYPE_CHECKING:
    from miappe.model.study import Study


class DataFile(Base):
    __tablename__ = "data_file_table"

    version: Mapped[Optional[str]]
    link: Mapped[Optional[str]]

    # Relationship
    study_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("study_table.id"))
    study: Mapped[Optional["Study"]] = relationship(
        "Study",
        back_populates="data_files",
        lazy="selectin",
        info=dto_field("read-only")
    )
