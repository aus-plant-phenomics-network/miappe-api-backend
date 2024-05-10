from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from litestar import get
from sqlalchemy.ext.asyncio import AsyncSession

from src.model import Investigation
from src.router.base import BaseController, read_items_by_attrs
from src.router.utils.dto import DTOGenerator

__all__ = ("InvestigationController",)

if TYPE_CHECKING:
    pass

InvestigationDTO = DTOGenerator[Investigation](
    read_kwargs={"max_nested_depth": 0, "rename_strategy": "camel"}, write_kwargs={"rename_strategy": "camel"}
)


class InvestigationController(BaseController[Investigation]):
    path = "/investigation"
    dto = InvestigationDTO.write_dto
    return_dto = InvestigationDTO.read_dto

    @get("/")
    async def get_items(self, table: Any, transaction: "AsyncSession", title: str | None) -> Sequence[Investigation]:
        return await read_items_by_attrs(transaction, Investigation, title=title)
