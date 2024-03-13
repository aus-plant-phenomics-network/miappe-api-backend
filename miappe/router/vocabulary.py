from typing import Sequence, TYPE_CHECKING

from litestar import get
from sqlalchemy.ext.asyncio import AsyncSession

from miappe.model import Vocabulary
from miappe.router.utils.CRUD import read_items_by_attrs
from miappe.router.utils.DTO import VocabularyDTO

if TYPE_CHECKING:
    pass
from miappe.router.base import BaseController


class VocabularyController(BaseController):
    path = "/vocabulary"

    def __init__(self, *args, **kwargs):
        super().__init__(Vocabulary, VocabularyDTO, *args, **kwargs)

    @get(return_dto=VocabularyDTO.read_dto)
    async def get_vocabulary(self,
                             transaction: "AsyncSession",
                             namespace: str | None = None,
                             external_reference: str | None = None) -> Sequence[Vocabulary]:
        return await read_items_by_attrs(session=transaction, table=self.table, namespace=namespace,
                                         external_reference=external_reference)
