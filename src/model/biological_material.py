# from typing import TYPE_CHECKING, Optional
# from uuid import UUID

# from litestar.dto import dto_field
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship

# from src.model.base import Base

# __all__ = ("BiologicalMaterial",)


# if TYPE_CHECKING:
#     from src.model.method import Method
#     from src.model.variable import Variable


# class BiologicalMaterial(Base):
#     __tablename__: str = "biological_material_table"  # type: ignore[assignment]

#     id: Mapped[UUID] = mapped_column(ForeignKey("variable_table.id"), primary_key=True, info=dto_field("read-only"))
#     biological_location: Mapped[str | None]
#     material_source_id: Mapped[str | None]
#     material_source_doi: Mapped[str | None]
#     material_source_location: Mapped[str | None]
#     material_source_description: Mapped[str | None]

#     # Relationship
#     preprocessing_method_id: Mapped[UUID | None] = mapped_column(
#         ForeignKey("method_table.id"),
#     )
#     preprocessing_method: Mapped[Optional["Method"]] = relationship(
#         back_populates="biological_material",
#         lazy="selectin",
#         info=dto_field("read-only"),
#     )
#     variable: Mapped["Variable"] = relationship(
#         back_populates="biological_material",
#         lazy="selectin",
#         info=dto_field("read-only"),
#     )
