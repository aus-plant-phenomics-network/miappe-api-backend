from typing import TYPE_CHECKING, Sequence

from litestar import Controller, get, post
from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig
from sqlalchemy import select

from miappe.model import Vocabulary

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from uuid import UUID


class VocabularyReadDTO(SQLAlchemyDTO[Vocabulary]):
    config = SQLAlchemyDTOConfig(exclude={"device"})


class VocabularyWriteDTO(SQLAlchemyDTO[Vocabulary]):
    config = SQLAlchemyDTOConfig(exclude={"id", "device"})


class VocabularyController(Controller):
    path = "/vocabulary"

    @get(return_dto=VocabularyReadDTO)
    async def get_vocabulary(self, transaction: AsyncSession) -> Sequence[Vocabulary]:
        result = await transaction.execute(select(Vocabulary))
        return result.scalars().all()

    @get("/{id:UUID}, return_dto=DeviceReadDTO")
    async def get_vocabulary_by_id(self, transaction: AsyncSession, id: UUID) -> Vocabulary:
        result = await transaction.execute(select(Vocabulary).where(Vocabulary.id == id))
        return result.scalars().one()

    @post(dto=VocabularyWriteDTO, return_dto=VocabularyWriteDTO)
    async def add_vocabulary_item(self, transaction: AsyncSession, data: Vocabulary) -> Vocabulary:
        transaction.add(data)
        return data
