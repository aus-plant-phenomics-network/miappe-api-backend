from typing import TYPE_CHECKING, Optional
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.base import Base

__all__ = ("Method",)


if TYPE_CHECKING:
    from src.model.biological_material import BiologicalMaterial
    from src.model.device import Device
    from src.model.observed_variable import ObservedVariable
    from src.model.vocabulary import Vocabulary


class Method(Base):
    __tablename__: str = "method_table"  # type: ignore[assignment]

    # Relationships:
    method_type_id: Mapped[UUID | None] = mapped_column(ForeignKey("vocabulary_table.id", ondelete="SET NULL"))
    method_type: Mapped[Optional["Vocabulary"]] = relationship(
        back_populates="method", lazy=None, info=dto_field("read-only")
    )

    device_id: Mapped[UUID | None] = mapped_column(ForeignKey("device_table.id", ondelete="SET NULL"))
    device: Mapped[Optional["Device"]] = relationship(lazy=None, info=dto_field("read-only"))

    biological_material: Mapped[Optional["BiologicalMaterial"]] = relationship(
        back_populates="preprocessing_method",
        lazy=None,
        info=dto_field("read-only"),
    )
    observed_variable: Mapped[Optional["ObservedVariable"]] = relationship(
        back_populates="method", lazy=None, info=dto_field("read-only")
    )
