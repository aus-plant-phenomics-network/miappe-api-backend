import datetime
from typing import TYPE_CHECKING

from litestar.dto import dto_field
from sqlalchemy.orm import Mapped, relationship

from src.model import Base

__all__ = ("Investigation",)


if TYPE_CHECKING:
    from src.model.study import Study


class Investigation(Base):
    __tablename__ = "investigation_table"  # type: ignore[assignment]

    submission_date: Mapped[datetime.datetime | None]
    public_release_date: Mapped[datetime.datetime | None]
    license: Mapped[str | None]
    publication_doi: Mapped[str | None]
    website: Mapped[str | None]
    funding: Mapped[str | None]

    # Relationship
    studies: Mapped[list["Study"]] = relationship(
        "Study", back_populates="investigation", lazy="selectin", info=dto_field("read-only")
    )
