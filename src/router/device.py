import datetime
from collections.abc import Sequence
from typing import TYPE_CHECKING
from uuid import UUID

from litestar import get
from sqlalchemy import select

from src.model import Device, Vocabulary
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("DeviceController",)


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

DeviceDTO = DTOGenerator[Device](read_kwargs={"max_nested_depth": 0})


class DeviceController(BaseController[Device]):
    path = "/device"
    dto = DeviceDTO.write_dto
    return_dto = DeviceDTO.read_dto

    @get(return_dto=DeviceDTO.read_dto)
    async def get_devices(
        self,
        transaction: "AsyncSession",
        name: str | None = None,
        device_type_id: UUID | None = None,
        device_type_name: str | None = None,
        brand: str | None = None,
        serial_number: str | None = None,
        startup_date: datetime.datetime | None = None,
        removal_date: datetime.datetime | None = None,
    ) -> Sequence[Device]:
        if device_type_name:
            stmt = (
                select(Device)
                .join_from(Device, Vocabulary, Device.device_type_id == Vocabulary.id)
                .where(Vocabulary.name == device_type_name)
            )
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
