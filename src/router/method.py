from collections.abc import Sequence

from litestar import get
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.model import Method, Vocabulary
from src.router.base import BaseController, read_items_by_attrs
from src.router.utils.dto import DTOGenerator

__all__ = ("MethodController",)


MethodDTO = DTOGenerator[Method](read_kwargs={"max_nested_depth": 1})


class MethodController(BaseController[Method]):
    path = "/method"
    dto = MethodDTO.read_dto
    return_dto = MethodDTO.write_dto

    @get(return_dto=MethodDTO.read_dto)
    async def get_items(
        self, transaction: AsyncSession, method_type_name: str | None = None, name: str | None = None
    ) -> Sequence[Method]:
        return await read_items_by_attrs(transaction, Method, name=name, method_type_name=method_type_name)
