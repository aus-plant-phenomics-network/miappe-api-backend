from typing import Sequence
from uuid import UUID

from litestar import Controller, get, post
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from miappe.model import Vocabulary, Method
from miappe.router.DTO import MethodWriteDTO, MethodReadDTO


class MethodController(Controller):
    path = "/method"

    @get(return_dto=MethodReadDTO)
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

    @get("/{id:uuid}", return_dto=MethodReadDTO)
    async def get_method_by_id(self, id: UUID, transaction: AsyncSession) -> Method:
        result = await transaction.execute(select(Method).where(Method.id == id))
        return result.scalars().one()

    @post(dto=MethodWriteDTO, return_dto=MethodWriteDTO)
    async def add_method_item(self, transaction: AsyncSession, data: Method) -> Method:
        transaction.add(data)
        return data
