from typing import Sequence
from uuid import UUID

from litestar import Controller, get, post, put, delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from miappe.model import Vocabulary, Unit
from miappe.router.utils.CRUD import read_item_by_id, create_item, update_item, delete_item
from miappe.router.utils.DTO import UnitDTO


class UnitController(Controller):
    path = "/unit"
    table: Unit

    @get(return_dto=UnitDTO.read_dto)
    async def get_unit(self,
                       transaction: AsyncSession,
                       unit_type_name: str | None = None,
                       symbol: str | None = None,
                       alternative_symbol: str | None = None
                       ) -> Sequence[Unit]:
        if unit_type_name:
            stmt = select(Unit).join_from(Unit, Vocabulary,
                                          Unit.unit_type_id == Vocabulary.id).where(
                Vocabulary.name == unit_type_name)
        else:
            stmt = select(Unit)

        if symbol:
            stmt = stmt.where(Unit.symbol == symbol)
        if alternative_symbol:
            stmt = stmt.where(Unit.alternative_symbol == alternative_symbol)
        result = await transaction.execute(stmt)
        return result.scalars().all()

    @get("/{id:uuid}", return_dto=UnitDTO.read_dto)
    async def get_unit_by_id(self, id: UUID, transaction: AsyncSession) -> Unit:
        return await read_item_by_id(session=transaction, id=id, table=self.table)

    @post(dto=UnitDTO.write_dto, return_dto=UnitDTO.write_dto)
    async def add_unit(self, transaction: AsyncSession, data: Unit) -> Unit:
        return await create_item(session=transaction, data=data)

    @put("/{id:uuid}", dto=UnitDTO.update_dto, return_dto=UnitDTO.read_dto)
    async def update_unit(self, transaction: AsyncSession, data: Unit, id: "UUID") -> Unit:
        return await update_item(session=transaction, id=id, table=self.table, data=data)

    @delete("/{id:uuid}")
    async def delete_unit(self, transaction: AsyncSession, id: "UUID") -> None:
        return await delete_item(session=transaction, id=id, table=self.table)
