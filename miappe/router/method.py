from typing import Sequence, TYPE_CHECKING
from uuid import UUID

from litestar import Controller, get, post, put, delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from miappe.model import Vocabulary, Method
from miappe.router.utils.CRUD import read_item_by_id, create_item, update_item, delete_item
from miappe.router.utils.DTO import MethodDTO

if TYPE_CHECKING:
    from sqlalchemy.orm import DeclarativeBase


class MethodController(Controller):
    path = "/method"
    table: "DeclarativeBase" = Method

    @get(return_dto=MethodDTO.read_dto)
    async def get_method(self,
                         transaction: AsyncSession,
                         method_type_name: str | None = None
                         ) -> Sequence[Method]:
        if method_type_name:
            stmt = select(Method).join_from(Method, Vocabulary,
                                            Method.method_type_id == Vocabulary.id).where(
                Vocabulary.name == method_type_name)
        else:
            stmt = select(Method)

        result = await transaction.execute(stmt)
        return result.scalars().all()

    @get("/{id:uuid}", return_dto=MethodDTO.read_dto)
    async def get_method_by_id(self, id: UUID, transaction: AsyncSession) -> Method:
        return await read_item_by_id(session=transaction, id=id, table=self.table)

    @post(dto=MethodDTO.write_dto, return_dto=MethodDTO.write_dto)
    async def add_method(self, transaction: AsyncSession, data: Method) -> Method:
        return await create_item(session=transaction, data=data)

    @put("/{id:uuid}", dto=MethodDTO.update_dto, return_dto=MethodDTO.read_dto)
    async def update_method(self, transaction: AsyncSession, data: Method, id: "UUID") -> Method:
        return await update_item(session=transaction, id=id, table=self.table, data=data)

    @delete("/{id:uuid}")
    async def delete_method(self, transaction: AsyncSession, id: "UUID") -> None:
        return await delete_item(session=transaction, id=id, table=self.table)
