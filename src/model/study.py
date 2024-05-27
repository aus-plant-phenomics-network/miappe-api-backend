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
    title: Mapped[str] = mapped_column(nullable=False)
    objective: Mapped[str] = mapped_column(nullable=False)
    start_date: Mapped[datetime.datetime | None]
    end_date: Mapped[datetime.datetime | None]

    # Relationship
    investigation_id: Mapped[UUID] = mapped_column(ForeignKey("investigation_table.id", ondelete="cascade"))
    investigation: Mapped[Optional["Investigation"]] = relationship(
        "Investigation",
        lazy=None,
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
    data_files: Mapped[list["DataFile"]] = relationship(
        "DataFile",
        secondary="study_data_file_table",
        lazy=None,
        info=dto_field("read-only"),
    )
    # experiments: Mapped[list["Experiment"]] = relationship(
    #     "Experiment", back_populates="study", lazy="selectin", info=dto_field("read-only")
    # )
