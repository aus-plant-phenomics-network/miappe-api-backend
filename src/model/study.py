import datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model import Base

if TYPE_CHECKING:
    from src.model.investigation import Investigation
    from src.model.variable import Variable
    from src.model.data_file import DataFile
    from src.model.experiment import Experiment
    from src.model.observation_unit import ObservationUnit


class Study(Base):
    __tablename__ = "study_table"  # type: ignore[assignment]
    start_date: Mapped[Optional[datetime.datetime]]
    end_date: Mapped[Optional[datetime.datetime]]
    objective: Mapped[str]

    # Relationship
    investigation_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("investigation_table.id"))
    investigation: Mapped[Optional["Investigation"]] = relationship(
        "Investigation",
        back_populates="studies",
        lazy="selectin",
        info=dto_field("read-only")
    )
    variables: Mapped[list["Variable"]] = relationship(
        "Variable",
        secondary="study_variable_table",
        back_populates="studies",
        lazy="selectin",
        info=dto_field("read-only")
    )
    data_files: Mapped[list["DataFile"]] = relationship(
        "DataFile",
        back_populates="study",
        lazy="selectin",
        info=dto_field("read-only")
    )
    experiments: Mapped[list["Experiment"]] = relationship(
        "Experiment",
        back_populates="study",
        lazy="selectin",
        info=dto_field("read-only")
    )
    observation_units: Mapped[list["ObservationUnit"]] = relationship(
        "ObservationUnit",
        back_populates="study",
        lazy="selectin",
        info=dto_field("read-only")
    )
