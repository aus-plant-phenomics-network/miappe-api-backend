from typing import Any, cast
from uuid import UUID

from litestar import get, post, put
from litestar.dto import DataclassDTO, DTOConfig
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.institution import Institution, InstitutionDataclass
from src.router.base import BaseController, read_item_by_id, read_items_by_attrs

__all__ = ("InstitutionController",)


class InstitutionDTO(DataclassDTO[InstitutionDataclass]):
    config = DTOConfig(rename_strategy="camel")


async def prepare_data_dict(session: AsyncSession, data: InstitutionDataclass) -> dict[str, Any]:
    data_dict = data.to_dict()
    data_dict.pop("parent_id")
    if len(data.parent_id) > 0:
        parents = await read_items_by_attrs(
            session=session, table=Institution, selectinload_attrs=[Institution.parents], id=data.parent_id
        )
        data_dict["parents"] = parents
    return data_dict


class InstitutionController(BaseController[Institution]):
    path = "/institution"
    dto = InstitutionDTO

    @get("/{id:uuid}")
    async def get_item_by_id(self, transaction: AsyncSession, id: UUID) -> InstitutionDataclass:
        data = await read_item_by_id(transaction, Institution, id, [Institution.parents])
        return InstitutionDataclass.from_orm(data)

    @post(dto=InstitutionDTO)
    async def create_item(self, transaction: AsyncSession, data: InstitutionDataclass) -> Institution:  # type: ignore[name-defined]
        data_dict = await prepare_data_dict(transaction, data)
        institution_data = Institution(**data_dict)
        transaction.add(institution_data)
        await transaction.flush()
        return institution_data

    @put("{id:uuid}", dto=InstitutionDTO)
    async def update_item(self, transaction: AsyncSession, data: InstitutionDataclass, id: UUID) -> Institution:
        # Fetch item
        item = cast(
            Institution,
            await read_item_by_id(
                session=transaction, table=Institution, id=id, selectinload_attrs=[Institution.parents]
            ),
        )
        # Fetch parents
        data_dict = await prepare_data_dict(transaction, data)
        for k, v in data_dict.items():
            setattr(item, k, v)
        return item
