from typing import Sequence
from uuid import UUID

from litestar import Controller, get, post
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from miappe.model import Device
from miappe.router.DTO import DeviceReadDTO, DeviceWriteDTO


class DeviceController(Controller):
    path = "/device"

    @get(return_dto=DeviceReadDTO)
    async def get_devices(self, transaction: AsyncSession) -> Sequence[Device]:
        result = await transaction.execute(select(Device))
        return result.scalars().all()

    @get("/{id:uuid}", return_dto=DeviceReadDTO)
    async def get_device_by_id(self, id: UUID, transaction: AsyncSession) -> Device | None:
        result = await transaction.execute(select(Device).where(Device.id == id))
        return result.scalars().one()

    @post(dto=DeviceWriteDTO, return_dto=DeviceWriteDTO)
    async def add_device(self, transaction: AsyncSession, data: Device) -> Device:
        transaction.add(data)
        return data
