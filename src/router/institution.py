import datetime
from dataclasses import dataclass, field
from typing import cast
from uuid import UUID

from litestar import Controller, delete, get, post, put
from litestar.dto import DataclassDTO, DTOConfig
from sqlalchemy import delete as remove
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.model import Institution

__all__ = ("InstitutionController",)


@dataclass
class InstitutionWriteData:
    id: UUID | None
    title: str
    description: str | None
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None
    institution_type_id: UUID | None
    parent_id: list[UUID] = field(default_factory=list[UUID])


class InstitutionWriteDTO(DataclassDTO[InstitutionWriteData]):
    config = DTOConfig(rename_strategy="camel")


class InstitutionController(Controller):
    path = "/institution"

    @get()
    async def get_item(self, transaction: AsyncSession) -> list[Institution]:
        stmt = select(Institution)
        result = await transaction.execute(stmt)
        return cast(list[Institution], result.scalars().all())

    @get("/{id:uuid}", return_dto=InstitutionWriteDTO)
    async def get_item_by_id(self, transaction: AsyncSession, id: UUID) -> InstitutionWriteData:
        stmt = select(Institution).where(Institution.id == id).options(selectinload(Institution.parents))
        result = await transaction.execute(stmt)
        data = result.scalars().one()
        return_data = InstitutionWriteData(
            id=data.id,
            title=data.title,
            description=data.description,
            created_at=data.created_at,
            updated_at=data.updated_at,
            institution_type_id=data.institution_type_id,
            parent_id=[],
        )
        if len(data.parents) > 0:
            return_data.parent_id = [item.id for item in data.parents]
        return return_data

    @post(dto=InstitutionWriteDTO)
    async def create_item(self, transaction: AsyncSession, data: InstitutionWriteData) -> None:  # type: ignore[name-defined]
        institution_data = Institution(
            title=data.title, description=data.description, institution_type_id=data.institution_type_id
        )
        if len(data.parent_id) > 0:
            stmt = select(Institution).where(Institution.id.in_(data.parent_id))
            result = await transaction.execute(stmt)
            parents: list[Institution] = cast(list[Institution], result.scalars().all())
            institution_data.parents = parents
        transaction.add(institution_data)
        return

    @put("{id:uuid}", dto=InstitutionWriteDTO)
    async def update_item(self, transaction: AsyncSession, data: InstitutionWriteData, id: UUID) -> None:
        # Fetch item
        stmt = select(Institution).where(Institution.id == id).options(selectinload(Institution.parents))
        result = await transaction.execute(stmt)
        item = result.scalars().one()
        # Fetch parents
        if len(data.parent_id) > 0:
            stmt = select(Institution).where(Institution.id.in_(data.parent_id))
            result = await transaction.execute(stmt)
            parents: list[Institution] = cast(list[Institution], result.scalars().all())
            item.parents = parents
        item.title = data.title
        item.description = data.description
        item.institution_type_id = data.institution_type_id
        item.updated_at = datetime.datetime.now(datetime.UTC)
        return

    @delete("{id:uuid}")
    async def delete_item(self, transaction: AsyncSession, id: UUID) -> None:
        stmt = remove(Institution).where(Institution.id == id)
        await transaction.execute(stmt)
        return
