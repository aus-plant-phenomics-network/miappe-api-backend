from collections.abc import Sequence

from litestar import get
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.model import Unit, Vocabulary
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("UnitController",)

UnitDTO = DTOGenerator[Unit]()


class UnitController(BaseController[Unit]):
    path = "/unit"
    dto = UnitDTO.write_dto
    return_dto = UnitDTO.read_dto

    @get(return_dto=UnitDTO.read_dto)
    async def get_unit(
        self,
        transaction: AsyncSession,
        name: str | None = None,
        unit_type_name: str | None = None,
        symbol: str | None = None,
        alternative_symbol: str | None = None,
    ) -> Sequence[Unit]:
        stmt = select(Unit).where(Vocabulary.name == unit_type_name) if unit_type_name else select(Unit)
        if name:
            stmt = stmt.where(Unit.name == name)
        if symbol:
            stmt = stmt.where(Unit.symbol == symbol)
        if alternative_symbol:
            stmt = stmt.where(Unit.alternative_symbol == alternative_symbol)
        result = await transaction.execute(stmt)
        return result.scalars().all()
