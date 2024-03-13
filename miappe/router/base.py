from typing import TYPE_CHECKING
from uuid import UUID

from litestar import Controller, get, put, post, delete
from sqlalchemy.orm import DeclarativeBase

from miappe.router.utils.CRUD import read_item_by_id, create_item, delete_item, update_item

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from miappe.router.utils.DTO import DTOGenerator


class BaseController(Controller):
    def __init__(self, table: DeclarativeBase, dto_factory: "DTOGenerator", *args, **kwargs):
        self.table = table

        @get("/{id:uuid}", return_dto=dto_factory.read_dto)
        async def _get_item_by_id(self, transaction: "AsyncSession", id: UUID) -> table:
            return await read_item_by_id(session=transaction, table=table, id=id)

        @post(dto=dto_factory.write_dto, return_dto=dto_factory.write_dto)
        async def _add_item(self, transaction: "AsyncSession", data: table) -> table:
            return await create_item(session=transaction, data=data)

        @put("/{id:uuid}", dto=dto_factory.update_dto, return_dto=dto_factory.read_dto)
        async def _update_item(self,
                               transaction: "AsyncSession",
                               id: UUID,
                               data: table) -> table:
            result = await update_item(session=transaction, id=id, data=data, table=table)
            return result

        @delete("/{id:uuid}")
        async def _delete_item(self, transaction: "AsyncSession", id: UUID) -> None:
            await delete_item(session=transaction, id=id, table=table)

        self.get_item_by_id = _get_item_by_id
        self.add_item = _add_item
        self.update_item = _update_item
        self.delete_item = _delete_item

        super().__init__(*args, **kwargs)
