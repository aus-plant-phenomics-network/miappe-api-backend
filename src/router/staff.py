from typing import Any, cast
from uuid import UUID

from litestar import get, post, put
from litestar.dto import DataclassDTO, DTOConfig
from sqlalchemy.ext.asyncio import AsyncSession

from src.model.institution import Institution
from src.model.staff import Staff, StaffDataclass
from src.router.base import BaseController, read_item_by_id, read_items_by_attrs

__all__ = ("StaffController",)


class StaffDTO(DataclassDTO[StaffDataclass]):
    config = DTOConfig(rename_strategy="camel")


async def prepare_data_dict(session: AsyncSession, data: StaffDataclass) -> dict[str, Any]:
    data_dict = data.to_dict()
    data_dict.pop("institution_id")
    if len(data.institution_id) > 0:
        institutions = await read_items_by_attrs(session=session, table=Institution, id=data.institution_id)
        data_dict["institutions"] = institutions
    return data_dict


class StaffController(BaseController[Staff]):
    path = "/staff"
    dto = StaffDTO

    @get("/{id:uuid}")
    async def get_item_by_id(self, transaction: AsyncSession, id: UUID) -> StaffDataclass:
        data = await read_item_by_id(transaction, Staff, id, [Staff.institutions])
        return StaffDataclass.from_orm(data)

    @post(dto=StaffDTO)
    async def create_item(self, transaction: AsyncSession, data: StaffDataclass) -> Staff:  # type: ignore[name-defined]
        data_dict = await prepare_data_dict(transaction, data)
        staff_data = Staff(**data_dict)
        transaction.add(staff_data)
        await transaction.flush()
        return staff_data

    @put("{id:uuid}", dto=StaffDTO)
    async def update_item(self, transaction: AsyncSession, data: StaffDataclass, id: UUID) -> Staff:
        # Fetch item
        item = cast(
            Staff,
            await read_item_by_id(session=transaction, table=Staff, id=id, selectinload_attrs=[Staff.institutions]),
        )
        # Fetch
        data_dict = await prepare_data_dict(transaction, data)
        for k, v in data_dict.items():
            setattr(item, k, v)
        return item
