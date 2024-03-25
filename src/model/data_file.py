from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model import Base

__all__ = ("DataFile",)


if TYPE_CHECKING:
    from src.model.study import Study


class DataFile(Base):
    __tablename__ = "data_file_table"  # type: ignore[assignment]

    version: Mapped[str | None]
    link: Mapped[str | None]

    # Relationship
    study_id: Mapped[UUID | None] = mapped_column(ForeignKey("study_table.id"))
    study: Mapped[Optional["Study"]] = relationship(
        "Study", back_populates="data_files", lazy="selectin", info=dto_field("read-only")
    )
