import datetime
from typing import Optional

from sqlalchemy.orm import Mapped

from miappe.model import Base


class Investigation(Base):
    __tablename__ = "investigation_table"

    submission_date: Mapped[Optional[datetime.datetime]]
    public_release_date: Mapped[Optional[datetime.datetime]]
    license: Mapped[Optional[str]]
    publication_doi: Mapped[Optional[str]]
    website: Mapped[Optional[str]]
    funding: Mapped[Optional[str]]