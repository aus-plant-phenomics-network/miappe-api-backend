from typing import TYPE_CHECKING, Sequence

from litestar import get
from sqlalchemy.ext.asyncio import AsyncSession

from miappe.model import Variable
from miappe.router.base import read_items_by_attrs
from miappe.router.utils.DTO import DTOGenerator

from miappe.router.base import BaseController

VariableDTO = DTOGenerator[Variable]()


class VariableController(BaseController[Variable]):
    path = "/variable"

    @get(return_dto=VariableDTO.read_dto)
    async def get_variable(
        self,
        transaction: AsyncSession,
    ) -> Sequence[Variable]:
        return await read_items_by_attrs(session=transaction, table=Variable)
