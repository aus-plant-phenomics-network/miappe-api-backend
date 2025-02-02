from dataclasses import dataclass, field
from typing import TYPE_CHECKING, cast
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.base import Base, BaseDataclass, Serialisable

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
    __tablename__ = "data_file_table"

    data_file_description: Mapped[str] = mapped_column(nullable=False)
    data_file_version: Mapped[str] = mapped_column(nullable=False)
    data_file_link: Mapped[str] = mapped_column(nullable=False)

    # Relationship
    studies: Mapped[list["Study"]] = relationship(
        secondary="study_data_file_table",
        lazy=None,
        info=dto_field("read-only"),
        back_populates="data_files",
    )


@dataclass(kw_only=True)
class DataFileDataclass(BaseDataclass):
    data_file_description: str
    data_file_version: str
    data_file_link: str
    study_id: list[UUID] = field(default_factory=list[UUID])

    @classmethod
    def from_orm(cls, data: Serialisable) -> "DataFileDataclass":
        data = cast(DataFile, data)
        data_dict = data.to_dict()
        if len(data.studies) > 0:
            data_dict["study_id"] = [item.id for item in data.studies]
        return cls(**data_dict)
