# from collections.abc import Sequence

# from litestar import get
# from sqlalchemy.ext.asyncio import AsyncSession

# from src.model import Variable
# from src.router.base import BaseController, read_items_by_attrs
# from src.router.utils.dto import DTOGenerator

# __all__ = ("VariableController",)


# VariableDTO = DTOGenerator[Variable]()


# class VariableController(BaseController[Variable]):
#     path = "/variable"
#     dto = VariableDTO.read_dto
#     return_dto = VariableDTO.write_dto

#     @get(return_dto=VariableDTO.read_dto)
#     async def get_items(self, transaction: AsyncSession, name: str | None = None) -> Sequence[Variable]:
#         return await read_items_by_attrs(session=transaction, table=Variable, name=name)
