import datetime
from typing import Sequence, TYPE_CHECKING
from uuid import UUID

from litestar import Controller, get, post, put, delete
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from miappe.model import Device, Vocabulary
from miappe.router.utils.CRUD import create_item, read_item_by_id, update_item, delete_item
from miappe.router.utils.DTO import DeviceDTO

if TYPE_CHECKING:
    from sqlalchemy.orm import DeclarativeBase


class DeviceController(Controller):
    path = "/device"
    table: "DeclarativeBase" = Device

    @get("/{id:uuid}", return_dto=DeviceDTO.read_dto)
    async def get_device_by_id(self, id: UUID, transaction: AsyncSession) -> Device | None:
        return await read_item_by_id(session=transaction, table=self.table, id=id)

    @get(return_dto=DeviceDTO.read_dto)
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

    @post(dto=DeviceDTO.write_dto, return_dto=DeviceDTO.read_dto)
    async def add_device(self, transaction: AsyncSession, data: Device) -> Device:
        return await create_item(session=transaction, data=data)

    @put("/{id:uuid}", dto=DeviceDTO.update_dto, return_dto=DeviceDTO.read_dto)
    async def update_device(self,
                            transaction: AsyncSession,
                            id: UUID,
                            data: Device) -> Device:
        result = await update_item(session=transaction, id=id, data=data, table=self.table)
        return result

    @delete("/{id:uuid}")
    async def delete_device(self, transaction: AsyncSession, id: UUID) -> None:
        await delete_item(session=transaction, id=id, table=self.table)
