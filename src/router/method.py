from collections.abc import Sequence

from litestar import get
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.model import Method, Vocabulary
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("MethodController",)


MethodDTO = DTOGenerator[Method](read_kwargs={"max_nested_depth": 1})


class MethodController(BaseController[Method]):
    path = "/method"
    dto = MethodDTO.read_dto
    return_dto = MethodDTO.write_dto

    @get(return_dto=MethodDTO.read_dto)
    async def get_method(
        self, transaction: AsyncSession, method_type_name: str | None = None, name: str | None = None
    ) -> Sequence[Method]:
        stmt = select(Method).where(Vocabulary.name == method_type_name) if method_type_name else select(Method)
        if name:
            stmt = stmt.where(Method.name == name)

        result = await transaction.execute(stmt)
        return result.scalars().all()
