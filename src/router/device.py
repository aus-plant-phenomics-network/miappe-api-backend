from src.model import Device
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("DeviceController",)


DeviceDTO = DTOGenerator[Device](read_kwargs={"max_nested_depth": 1})


class DeviceController(BaseController[Device]):
    path = "/device"
    dto = DeviceDTO.write_dto
    return_dto = DeviceDTO.read_dto
