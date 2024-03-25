from typing import Any, Sequence

from litestar import get
from sqlalchemy.ext.asyncio import AsyncSession

from src.model import Vocabulary
from src.router.base import BaseController
from src.router.base import read_items_by_attrs
from src.router.utils.DTO import DTOGenerator

VocabularyDTO = DTOGenerator[Vocabulary]()


class VocabularyController(BaseController[Vocabulary]):
    path = "/vocabulary"
    dto = VocabularyDTO.read_dto
    return_dto = VocabularyDTO.write_dto

    @get(return_dto=VocabularyDTO.read_dto)
    async def get_vocabulary(
            self,
            transaction: "AsyncSession",
            table: Any,
            name: str | None = None,
            namespace: str | None = None,
            external_reference: str | None = None,
    ) -> Sequence[Vocabulary]:
        return await read_items_by_attrs(
            session=transaction,
            table=table,
            namespace=namespace,
            external_reference=external_reference,
            name=name,
        )
