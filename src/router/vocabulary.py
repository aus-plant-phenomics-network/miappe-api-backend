from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from litestar import get

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

from src.model import Vocabulary
from src.router.base import BaseController, read_items_by_attrs
from src.router.utils.dto import DTOGenerator

__all__ = ("VocabularyController",)


VocabularyDTO = DTOGenerator[Vocabulary]()


class VocabularyController(BaseController[Vocabulary]):
    path = "/vocabulary"
    dto = VocabularyDTO.read_dto
    return_dto = VocabularyDTO.write_dto

    @get(return_dto=VocabularyDTO.read_dto)
    async def get_items(
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
