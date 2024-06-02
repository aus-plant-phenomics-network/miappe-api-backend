from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, cast
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import UUID as UUID_SQL
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.base import Base, BaseDataclass, Serialisable

__all__ = ("Variable",)


if TYPE_CHECKING:
    from src.model.device import Device
    from src.model.study import Study
    from src.model.unit import Unit

study_variable_table = Table(
    "study_variable_table",
    Base.metadata,
    Column("study_id", UUID_SQL, ForeignKey("study_table.id", ondelete="cascade"), primary_key=True),
    Column("variable_id", UUID_SQL, ForeignKey("variable_table.id", ondelete="cascade"), primary_key=True),
)


class Variable(Base):
    __tablename__: str = "variable_table"
    __mapper_args__ = {
        "polymorphic_identity": "variable",
        "polymorphic_on": "type",
    }
    description: Mapped[str | None]
    type: Mapped[str]
    time_interval: Mapped[str | None]
    sample_interval: Mapped[str | None]
    device_id: Mapped[UUID | None] = mapped_column(ForeignKey("device_table.id", ondelete="SET NULL"))
    device: Mapped[Optional["Device"]] = relationship(
        lazy=None,
        info=dto_field("read-only"),
    )
    unit_id: Mapped[UUID | None] = mapped_column(ForeignKey("unit_table.id", ondelete="SET NULL"))
    unit: Mapped[Optional["Unit"]] = relationship(
        lazy=None,
        info=dto_field("read-only"),
    )

    # Variable to study relationship
    studies: Mapped[list["Study"]] = relationship(
        secondary="study_variable_table",
        back_populates="variables",
        lazy=None,
        info=dto_field("read-only"),
    )


@dataclass(kw_only=True)
class VariableDataclass(BaseDataclass):
    description: str | None = field(default=None)
    type: str | None = field(default=None)
    time_interval: str | None = field(default=None)
    sample_interval: str | None = field(default=None)
    device_id: UUID | None = field(default=None)
    unit_id: UUID | None = field(default=None)
    study_id: list[UUID] = field(default_factory=list[UUID])

    @classmethod
    def from_orm(cls, data: Serialisable) -> "VariableDataclass":
        data = cast(Variable, data)
        data_dict = data.to_dict()
        if len(data.studies) > 0:
            data_dict["study_id"] = [item.id for item in data.studies]
        return cls(**data_dict)
