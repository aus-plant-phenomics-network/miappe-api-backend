import datetime
from typing import Optional, TYPE_CHECKING

from litestar.dto import dto_field
from sqlalchemy.orm import Mapped, relationship

from miappe.model import Base

if TYPE_CHECKING:
    from miappe.model.study import Study


class Investigation(Base):
    __tablename__ = "investigation_table"  # type: ignore[assignment]

    submission_date: Mapped[Optional[datetime.datetime]]
    public_release_date: Mapped[Optional[datetime.datetime]]
    license: Mapped[Optional[str]]
    publication_doi: Mapped[Optional[str]]
    website: Mapped[Optional[str]]
    funding: Mapped[Optional[str]]

    # Relationship
    studies: Mapped[list["Study"]] = relationship(
        "Study", back_populates="investigation", lazy="selectin", info=dto_field("read-only")
    )
