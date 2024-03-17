from typing import TYPE_CHECKING, Sequence

from litestar import get
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from miappe.model import Method, Vocabulary
from miappe.router.base import BaseController
from miappe.router.utils.DTO import DTOGenerator


MethodDTO = DTOGenerator[Method]()


class MethodController(BaseController[Method]):
    path = "/method"

    @get(return_dto=MethodDTO.read_dto)
    async def get_method(
        self, transaction: AsyncSession, method_type_name: str | None = None
    ) -> Sequence[Method]:
        if method_type_name:
            stmt = (
                select(Method)
                .join_from(Method, Vocabulary, Method.method_type_id == Vocabulary.id)
                .where(Vocabulary.name == method_type_name)
            )
        else:
            stmt = select(Method)

        result = await transaction.execute(stmt)
        return result.scalars().all()
