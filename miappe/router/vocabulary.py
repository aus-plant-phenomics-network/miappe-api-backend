from typing import Sequence, TYPE_CHECKING
from uuid import UUID

from litestar import Controller, get, post, put, delete
from sqlalchemy.ext.asyncio import AsyncSession

from miappe.model import Vocabulary
from miappe.router.utils.CRUD import create_item, read_item_by_id, update_item, delete_item, read_items_by_attrs
from miappe.router.utils.DTO import VocabularyDTO

if TYPE_CHECKING:
    from sqlalchemy.orm import DeclarativeBase


class VocabularyController(Controller):
    path = "/vocabulary"
    table: "DeclarativeBase" = Vocabulary

    @get(return_dto=VocabularyDTO.read_dto)
    async def get_vocabulary(self,
                             transaction: "AsyncSession",
                             namespace: str | None = None,
                             external_reference: str | None = None) -> Sequence[Vocabulary]:
        return await read_items_by_attrs(session=transaction, table=self.table, namespace=namespace,
                                         external_reference=external_reference)

    @get("/{id:uuid}", return_dto=VocabularyDTO.read_dto)
    async def get_vocabulary_by_id(self, id: UUID, transaction: AsyncSession) -> Vocabulary:
        return await read_item_by_id(session=transaction, table=self.table, id=id)

    @post(dto=VocabularyDTO.write_dto, return_dto=VocabularyDTO.read_dto)
    async def add_vocabulary_item(self, transaction: AsyncSession, data: Vocabulary) -> Vocabulary:
        return await create_item(session=transaction, data=data)

    @put("/{id:uuid}", dto=VocabularyDTO.update_dto, return_dto=VocabularyDTO.read_dto)
    async def update_vocabulary_item(self, transaction: AsyncSession, data: Vocabulary, id: "UUID") -> Vocabulary:
        return await update_item(session=transaction, id=id, table=self.table, data=data)

    @delete("/{id:uuid}")
    async def delete_item(self, transaction: AsyncSession, id: "UUID") -> None:
        return await delete_item(session=transaction, id=id, table=self.table)
