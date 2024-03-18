import datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from miappe.model import Base

if TYPE_CHECKING:
    from miappe.model.investigation import Investigation
    from miappe.model.variable import Variable

class Study(Base):
    __tablename__ = "study_table"
    start_date: Mapped[Optional[datetime.datetime]]
    end_date: Mapped[Optional[datetime.datetime]]
    objective: Mapped[str]
    investigation_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("investigation_table.id"))

    # Relationship
    investigation: Mapped[Optional["Investigation"]] = relationship(
        "Investigation",
        back_populates="study",
        lazy="selectin",
        info=dto_field("read-only")
    )
    variable: Mapped[list["Variable"]] = relationship(
        "Variable",
        secondary="study_variable_table",
        back_populates="study",
        lazy="selectin",
        info=dto_field("read-only")
    )
