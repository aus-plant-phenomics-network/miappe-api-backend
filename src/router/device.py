import datetime
from collections.abc import Sequence
from typing import TYPE_CHECKING
from uuid import UUID

from litestar import get
from sqlalchemy import select

from src.model import Device, Vocabulary
from src.router.base import BaseController, read_items_by_attrs
from src.router.utils.dto import DTOGenerator

__all__ = ("DeviceController",)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

DeviceDTO = DTOGenerator[Device](read_kwargs={"max_nested_depth": 1})


class DeviceController(BaseController[Device]):
    path = "/device"
    dto = DeviceDTO.write_dto
    return_dto = DeviceDTO.read_dto

    @get(return_dto=DeviceDTO.read_dto)
    async def get_items(
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
        return await read_items_by_attrs(transaction, Device, name=name, device_type_id=device_type_id, device_type_name=device_type_name, brand=brand, serial_number=serial_number, startup_date=startup_date, removal_date=removal_date)
