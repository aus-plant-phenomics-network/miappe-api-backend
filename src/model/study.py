import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model import Base

__all__ = ("Study",)

if TYPE_CHECKING:
    from src.model.data_file import DataFile

    #     from src.model.experiment import Experiment
    #     from src.model.variable import Variable
    from src.model.investigation import Investigation


class Study(Base):
    __tablename__ = "study_table"  # type: ignore[assignment]
    start_date: Mapped[datetime.datetime | None]
    end_date: Mapped[datetime.datetime | None]
    objective: Mapped[str]

    # Relationship
    investigation_id: Mapped[UUID | None] = mapped_column(ForeignKey("investigation_table.id", ondelete="cascade"))
    investigation: Mapped[Optional["Investigation"]] = relationship(
        "Investigation",
        lazy="selectin",
        info=dto_field("read-only"),
        back_populates="studies",
    )
    # variables: Mapped[list["Variable"]] = relationship(
    #     "Variable",
    #     secondary="study_variable_table",
    #     back_populates="studies",
    #     lazy="selectin",
    #     info=dto_field("read-only"),
    # )
    data_files: Mapped[list["DataFile"]] = relationship("DataFile", lazy="selectin", info=dto_field("read-only"))
    # experiments: Mapped[list["Experiment"]] = relationship(
    #     "Experiment", back_populates="study", lazy="selectin", info=dto_field("read-only")
    # )
