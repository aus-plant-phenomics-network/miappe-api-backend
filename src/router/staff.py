from typing import TYPE_CHECKING

from src.model import Staff
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("StaffController",)


StaffDTO = DTOGenerator[Staff](read_kwargs={"max_nested_depth": 1})


class StaffController(BaseController[Staff]):
    path = "/staff"
    dto = StaffDTO.write_dto
    return_dto = StaffDTO.read_dto
