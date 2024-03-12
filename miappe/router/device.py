import datetime
from typing import Sequence
from uuid import UUID

from litestar import Controller, get, post, put
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from miappe.model import Device, Vocabulary
from miappe.router.DTO import DeviceReadDTO, DeviceWriteDTO


class DeviceController(Controller):
    path = "/device"

    @get("/{id:uuid}", return_dto=DeviceReadDTO)
    async def get_device_by_id(self, id: UUID, transaction: AsyncSession) -> Device | None:
        result = await transaction.execute(select(Device).where(Device.id == id))
        return result.scalars().one()

    @get(return_dto=DeviceReadDTO)
    async def get_devices(self,
                          transaction: AsyncSession,
                          name: str | None = None,
                          device_type_id: UUID | None = None,
                          device_type_name: str | None = None,
                          brand: str | None = None,
                          serial_number: str | None = None,
                          startup_date: datetime.datetime | None = None,
                          removal_date: datetime.datetime | None = None
                          ) -> Sequence[Device]:
        if device_type_name:
            stmt = select(Device).join_from(Device, Vocabulary, Device.device_type_id == Vocabulary.id).where(
                Vocabulary.name == device_type_name)
        else:
            stmt = select(Device)
        if name:
            stmt = stmt.where(Device.name == name)
        if device_type_id:
            stmt = stmt.where(Device.device_type_id == device_type_id)
        if brand:
            stmt = stmt.where(Device.brand == brand)
        if serial_number:
            stmt = stmt.where(Device.serial_number == serial_number)
        if startup_date:
            stmt = stmt.where(Device.startup_date == startup_date)
        if removal_date:
            stmt = stmt.where(Device.removal_date == removal_date)
        items = await transaction.execute(stmt)
        return items.scalars().all()

    @post(dto=DeviceWriteDTO, return_dto=DeviceWriteDTO)
    async def add_device(self, transaction: AsyncSession, data: Device) -> Device:
        transaction.add(data)
        return data

    @put("/{id:uuid}", dto=DeviceWriteDTO, return_dto=DeviceReadDTO)
    async def update_device(self,
                            transaction: AsyncSession,
                            id: UUID,
                            data: Device) -> Device:
        data.updated_at = datetime.datetime.now(datetime.timezone.utc)
        update_data = {k: v for k, v in data.to_dict().items() if v}
        stmt = update(Device).where(Device.id == id).values(update_data)
        await transaction.execute(stmt)

        stmt = select(Device).where(Device.id == id)
        result = await transaction.execute(stmt)

        return result.scalars().one()
