from src.model import Unit
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("UnitController",)

UnitDTO = DTOGenerator[Unit]()


class UnitController(BaseController[Unit]):
    path = "/unit"
    dto = UnitDTO.write_dto
    return_dto = UnitDTO.read_dto
