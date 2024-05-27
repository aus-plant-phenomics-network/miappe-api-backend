from typing import Any, cast
from uuid import UUID

from litestar import get, post, put
from litestar.dto import DataclassDTO, DTOConfig
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.data_file import DataFile, DataFileDataclass
from src.model.study import Study
from src.router.base import BaseController, read_item_by_id, read_items_by_attrs

__all__ = ("DataFileController",)


class DataFileDTO(DataclassDTO[DataFileDataclass]):
    config = DTOConfig(rename_strategy="camel")


async def prepare_data_dict(session: AsyncSession, data: DataFileDataclass) -> dict[str, Any]:
    data_dict = data.to_dict()
    data_dict.pop("study_id")
    if len(data.study_id) > 0:
        studies = await read_items_by_attrs(session=session, table=Study, id=data.study_id)
        data_dict["studies"] = studies
    return data_dict


class DataFileController(BaseController[DataFile]):
    path = "/dataFile"
    dto = DataFileDTO

    @get("/{id:uuid}")
    async def get_item_by_id(self, transaction: AsyncSession, id: UUID) -> DataFileDataclass:
        data = await read_item_by_id(transaction, DataFile, id, [DataFile.studies])
        return DataFileDataclass.from_orm(data)

    @post(dto=DataFileDTO)
    async def create_item(self, transaction: AsyncSession, data: DataFileDataclass) -> DataFile:  # type: ignore[name-defined]
        data_dict = await prepare_data_dict(transaction, data)
        data_file_data = DataFile(**data_dict)
        transaction.add(data_file_data)
        await transaction.flush()
        return data_file_data

    @put("{id:uuid}", dto=DataFileDTO)
    async def update_item(self, transaction: AsyncSession, data: DataFileDataclass, id: UUID) -> DataFile:
        # Fetch item
        item = cast(
            DataFile,
            await read_item_by_id(session=transaction, table=DataFile, id=id, selectinload_attrs=[DataFile.studies]),
        )
        # Fetch parents
        data_dict = await prepare_data_dict(transaction, data)
        for k, v in data_dict.items():
            setattr(item, k, v)
        return item
