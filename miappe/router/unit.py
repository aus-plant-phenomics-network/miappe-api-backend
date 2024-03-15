from typing import Sequence, TYPE_CHECKING

from litestar import get
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from miappe.model import Vocabulary, Unit
from miappe.router.utils.DTO import UnitDTO

if TYPE_CHECKING:
    pass

from miappe.router.base import BaseController


class UnitController(BaseController[Unit]):
    path = "/unit"

    @get(return_dto=UnitDTO.read_dto)
    async def get_unit(
        self,
        transaction: AsyncSession,
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

        if symbol:
            stmt = stmt.where(Unit.symbol == symbol)
        if alternative_symbol:
            stmt = stmt.where(Unit.alternative_symbol == alternative_symbol)
        result = await transaction.execute(stmt)
        return result.scalars().all()
