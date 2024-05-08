from collections.abc import Sequence

from litestar import get
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.model import Unit, Vocabulary
from src.router.base import BaseController, read_items_by_attrs
from src.router.utils.dto import DTOGenerator

__all__ = ("UnitController",)

UnitDTO = DTOGenerator[Unit]()


class UnitController(BaseController[Unit]):
    path = "/unit"
    dto = UnitDTO.write_dto
    return_dto = UnitDTO.read_dto

    @get(return_dto=UnitDTO.read_dto)
    async def get_items(
        self,
        transaction: AsyncSession,
        name: str | None = None,
        unit_type_name: str | None = None,
        symbol: str | None = None,
        alternative_symbol: str | None = None,
    ) -> Sequence[Unit]:
        return read_items_by_attrs(transaction, Unit, name=name, unit_type_name=unit_type_name, symbol=symbol, alternative_symbol=alternative_symbol)
