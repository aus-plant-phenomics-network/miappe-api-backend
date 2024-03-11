from typing import TYPE_CHECKING, Sequence

from litestar import Controller, get
from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig
from sqlalchemy import select
from miappe.model import Device

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from uuid import UUID


class DeviceReadDTO(SQLAlchemyDTO[Device]):
    config = SQLAlchemyDTOConfig(exclude={"device_type_id"})


class DeviceController(Controller):
    path = "/device"

    @get(return_dto=DeviceReadDTO)
    async def get_devices(self, transaction: AsyncSession) -> Sequence[Device]:
        result = await transaction.execute(select(Device))
        return result.scalars().all()

    @get("/{id:UUID}, return_dto=DeviceReadDTO")
    async def get_device_by_id(self, transaction: AsyncSession, id: UUID) -> Device:
        result = await transaction.execute(select(Device).where(Device.id == id))
        return result.scalars().one()
