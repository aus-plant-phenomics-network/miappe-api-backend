from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, relationship

from src.model.base import Base, BaseDataclass

__all__ = ("DataFile", "DataFileDataclass")


if TYPE_CHECKING:
    from src.model.study import Study


study_data_file_table = Table(
    "study_data_file_table",
    Base.metadata,
    Column("study_id", UUID_SQL, ForeignKey("study_table.id", ondelete="cascade"), primary_key=True),
    Column("data_file_id", UUID_SQL, ForeignKey("data_file_table.id", ondelete="cascade"), primary_key=True),
)


class DataFile(Base):
    __tablename__ = "data_file_table"  # type: ignore[assignment]

    data_file_description: Mapped[str | None]
    data_file_version: Mapped[str | None]
    data_file_link: Mapped[str | None]

    # Relationship
    studies: Mapped[list["Study"]] = relationship(
        "Study",
        secondary="study_data_file_table",
        back_populates="data_files",
        lazy=None,
        info=dto_field("read-only"),
    )


@dataclass
class DataFileDataclass(BaseDataclass):
    data_file_description: str | None = field(default=None)
    data_file_version: str | None = field(default=None)
    data_file_link: str | None = field(default=None)
    study_id: list[UUID] = field(default_factory=list[UUID])

    @classmethod
    def from_orm(cls, data: DataFile) -> "DataFileDataclass":  # type: ignore[override]
        data_dict = data.to_dict()
        if len(data.studies) > 0:
            data_dict["study_id"] = [item.id for item in data.studies]
        return cls(**data_dict)
