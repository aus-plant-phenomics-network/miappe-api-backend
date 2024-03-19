from typing import Sequence

from litestar import get
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from miappe.model import Unit, Vocabulary
from miappe.router.base import BaseController
from miappe.router.utils.DTO import DTOGenerator

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
        if unit_type_name:
            stmt = (
                select(Unit)
                .join_from(Unit, Vocabulary, Unit.unit_type_id == Vocabulary.id)
                .where(Vocabulary.name == unit_type_name)
            )
        else:
            stmt = select(Unit)
        if name:
            stmt = stmt.where(Unit.name == name)
        if symbol:
            stmt = stmt.where(Unit.symbol == symbol)
        if alternative_symbol:
            stmt = stmt.where(Unit.alternative_symbol == alternative_symbol)
        result = await transaction.execute(stmt)
        return result.scalars().all()
