from typing import Any, cast
from uuid import UUID

from litestar import get, post, put
from litestar.dto import DataclassDTO, DTOConfig
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.environment import Environment, EnvironmentDataclass
from src.model.study import Study
from src.router.base import BaseController, read_item_by_id, read_items_by_attrs
from src.router.utils.dto import DTOGenerator

__all__ = ("EnvironmentController",)


class EnvironmentDTO(DataclassDTO[EnvironmentDataclass]):
    config = DTOConfig(rename_strategy="camel")


async def prepare_data_dict(session: AsyncSession, data: EnvironmentDataclass) -> dict[str, Any]:
    data_dict = data.to_dict()
    data_dict.pop("study_id")
    if len(data.study_id) > 0:
        studies = await read_items_by_attrs(session=session, table=Study, id=data.study_id)
        data_dict["studies"] = studies
    return data_dict


EnvironmentReturnDTO = DTOGenerator[Environment]()


class EnvironmentController(BaseController[Environment]):
    path = "/environment"
    dto = EnvironmentDTO
    return_dto = EnvironmentReturnDTO.read_dto

    @get("/{id:uuid}", return_dto=EnvironmentDTO)
    async def get_item_by_id(self, transaction: AsyncSession, id: UUID) -> EnvironmentDataclass:
        data = await read_item_by_id(transaction, Environment, id, [Environment.studies])
        return cast(EnvironmentDataclass, EnvironmentDataclass.from_orm(data))

    @post(dto=EnvironmentDTO)
    async def create_item(self, transaction: AsyncSession, data: EnvironmentDataclass) -> Environment:  # type: ignore[name-defined]
        data_dict = await prepare_data_dict(transaction, data)
        environment_data = Environment(**data_dict)
        transaction.add(environment_data)
        await transaction.flush()
        return environment_data

    @put("{id:uuid}", dto=EnvironmentDTO)
    async def update_item(self, transaction: AsyncSession, data: EnvironmentDataclass, id: UUID) -> Environment:
        # Fetch item
        item = cast(
            Environment,
            await read_item_by_id(
                session=transaction, table=Environment, id=id, selectinload_attrs=[Environment.studies]
            ),
        )
        # Fetch parents
        data_dict = await prepare_data_dict(transaction, data)
        for k, v in data_dict.items():
            setattr(item, k, v)
        return item
