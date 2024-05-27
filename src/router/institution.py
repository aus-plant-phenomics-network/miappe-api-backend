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
    country: str | None
    created_at: datetime.datetime | None
    updated_at: datetime.datetime | None
    institution_type_id: UUID | None
    parent_id: list[UUID] = field(default_factory=list[UUID])


class InstitutionWriteDTO(DataclassDTO[InstitutionWriteData]):
    config = DTOConfig(rename_strategy="camel")


async def get_institution_list(session: AsyncSession, id: list[UUID] | None = None) -> list[Institution]:
    stmt = select(Institution)
    if id:
        stmt = stmt.where(Institution.id.in_(id))
    result = await session.execute(stmt)
    return cast(list[Institution], result.scalars().all())


async def get_institution_by_id(
    session: AsyncSession, id: UUID, with_parents: bool = False, with_children: bool = False
) -> Institution:
    stmt = select(Institution).where(Institution.id == id)
    if with_parents:
        stmt = stmt.options(selectinload(Institution.parents))
    if with_children:
        stmt = stmt.options(selectinload(Institution.children))
    result = await session.execute(stmt)
    return result.scalars().one()


class InstitutionController(Controller):
    path = "/institution"

    @get()
    async def get_item(self, transaction: AsyncSession) -> list[Institution]:
        return await get_institution_list(transaction)

    @get("/{id:uuid}", return_dto=InstitutionWriteDTO)
    async def get_item_by_id(self, transaction: AsyncSession, id: UUID) -> InstitutionWriteData:
        data = await get_institution_by_id(transaction, id, True)
        return_data = InstitutionWriteData(
            id=data.id,
            title=data.title,
            country=data.country,
            created_at=data.created_at,
            updated_at=data.updated_at,
            institution_type_id=data.institution_type_id,
            parent_id=[],
        )
        if len(data.parents) > 0:
            return_data.parent_id = [item.id for item in data.parents]
        return return_data

    @post(dto=InstitutionWriteDTO)
    async def create_item(self, transaction: AsyncSession, data: InstitutionWriteData) -> Institution:  # type: ignore[name-defined]
        institution_data = Institution(
            title=data.title, country=data.country, institution_type_id=data.institution_type_id
        )
        if len(data.parent_id) > 0:
            parents = await get_institution_list(transaction, data.parent_id)
            institution_data.parents = parents
        transaction.add(institution_data)
        return institution_data

    @put("{id:uuid}", dto=InstitutionWriteDTO)
    async def update_item(self, transaction: AsyncSession, data: InstitutionWriteData, id: UUID) -> Institution:
        # Fetch item
        item = await get_institution_by_id(transaction, id, True)
        # Fetch parents
        if len(data.parent_id) > 0:
            parents = await get_institution_list(transaction, data.parent_id)
            item.parents = parents
        item.title = data.title
        item.country = data.country
        item.institution_type_id = data.institution_type_id
        item.updated_at = datetime.datetime.now(datetime.UTC)
        return item

    @delete("{id:uuid}")
    async def delete_item(self, transaction: AsyncSession, id: UUID) -> None:
        stmt = remove(Institution).where(Institution.id == id)
        await transaction.execute(stmt)
        return
