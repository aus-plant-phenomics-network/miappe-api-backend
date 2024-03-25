from typing import Sequence

from litestar import get
from sqlalchemy.ext.asyncio import AsyncSession

from src.model import Variable
from src.router.base import BaseController
from src.router.base import read_items_by_attrs
from src.router.utils.DTO import DTOGenerator

VariableDTO = DTOGenerator[Variable]()


class VariableController(BaseController[Variable]):
    path = "/variable"
    dto = VariableDTO.read_dto
    return_dto = VariableDTO.write_dto

    @get(return_dto=VariableDTO.read_dto)
    async def get_variable(
            self,
            transaction: AsyncSession,
            name: str | None = None
    ) -> Sequence[Variable]:
        return await read_items_by_attrs(session=transaction, table=Variable, name=name)
