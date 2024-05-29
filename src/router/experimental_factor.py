from typing import Any, cast
from uuid import UUID

from litestar import get, post, put
from litestar.dto import DataclassDTO, DTOConfig
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.experimental_factor import ExperimentalFactor, ExperimentalFactorDataclass
from src.model.study import Study
from src.router.base import BaseController, read_item_by_id, read_items_by_attrs
from src.router.utils.dto import DTOGenerator

__all__ = ("ExperimentalFactorController",)


class ExperimentalFactorDTO(DataclassDTO[ExperimentalFactorDataclass]):
    config = DTOConfig(rename_strategy="camel")


async def prepare_data_dict(session: AsyncSession, data: ExperimentalFactorDataclass) -> dict[str, Any]:
    data_dict = data.to_dict()
    data_dict.pop("study_id")
    if len(data.study_id) > 0:
        studies = await read_items_by_attrs(session=session, table=Study, id=data.study_id)
        data_dict["studies"] = studies
    return data_dict


ExperimentalFactorReturnDTO = DTOGenerator[ExperimentalFactor]()


class ExperimentalFactorController(BaseController[ExperimentalFactor]):
    path = "/experimentalFactor"
    dto = ExperimentalFactorDTO
    return_dto = ExperimentalFactorReturnDTO.read_dto

    @get("/{id:uuid}", return_dto=ExperimentalFactorDTO)
    async def get_item_by_id(self, transaction: AsyncSession, id: UUID) -> ExperimentalFactorDataclass:
        data = await read_item_by_id(transaction, ExperimentalFactor, id, [ExperimentalFactor.studies])
        return cast(ExperimentalFactorDataclass, ExperimentalFactorDataclass.from_orm(data))

    @post(dto=ExperimentalFactorDTO)
    async def create_item(self, transaction: AsyncSession, data: ExperimentalFactorDataclass) -> ExperimentalFactor:  # type: ignore[name-defined]
        data_dict = await prepare_data_dict(transaction, data)
        experimental_factor_data = ExperimentalFactor(**data_dict)
        transaction.add(experimental_factor_data)
        await transaction.flush()
        return experimental_factor_data

    @put("{id:uuid}", dto=ExperimentalFactorDTO)
    async def update_item(
        self, transaction: AsyncSession, data: ExperimentalFactorDataclass, id: UUID
    ) -> ExperimentalFactor:
        # Fetch item
        item = cast(
            ExperimentalFactor,
            await read_item_by_id(
                session=transaction, table=ExperimentalFactor, id=id, selectinload_attrs=[ExperimentalFactor.studies]
            ),
        )
        # Fetch parents
        data_dict = await prepare_data_dict(transaction, data)
        for k, v in data_dict.items():
            setattr(item, k, v)
        return item
