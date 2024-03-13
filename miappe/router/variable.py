from typing import Sequence, TYPE_CHECKING
from uuid import UUID

from litestar import Controller, get, post, put, delete
from sqlalchemy.ext.asyncio import AsyncSession

from miappe.model import Variable
from miappe.router.utils.CRUD import read_item_by_id, create_item, update_item, delete_item, read_items_by_attrs
from miappe.router.utils.DTO import VariableDTO

if TYPE_CHECKING:
    from sqlalchemy.orm import DeclarativeBase


class VariableController(Controller):
    path = "/variable"
    table: "DeclarativeBase" = Variable

    @get(return_dto=VariableDTO.read_dto)
    async def get_variable(self,
                           transaction: AsyncSession,
                           ) -> Sequence[Variable]:
        return await read_items_by_attrs(session=transaction, table=self.table)

    @get("/{id:uuid}", return_dto=VariableDTO.read_dto)
    async def get_variable_by_id(self, id: UUID, transaction: AsyncSession) -> Variable:
        return await read_item_by_id(session=transaction, id=id, table=self.table)

    @post(dto=VariableDTO.write_dto, return_dto=VariableDTO.write_dto)
    async def add_variable(self, transaction: AsyncSession, data: Variable) -> Variable:
        return await create_item(session=transaction, data=data)

    @put("/{id:uuid}", dto=VariableDTO.update_dto, return_dto=VariableDTO.read_dto)
    async def update_variable(self, transaction: AsyncSession, data: Variable, id: "UUID") -> Variable:
        return await update_item(session=transaction, id=id, table=self.table, data=data)

    @delete("/{id:uuid}")
    async def delete_variable(self, transaction: AsyncSession, id: "UUID") -> None:
        return await delete_item(session=transaction, id=id, table=self.table)
