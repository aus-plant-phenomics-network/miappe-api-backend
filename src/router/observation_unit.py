from typing import TYPE_CHECKING

from src.model import ObservationUnit
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("ObservationUnitController",)

if TYPE_CHECKING:
    pass

ObservationUnitDTO = DTOGenerator[ObservationUnit](read_kwargs={"max_nested_depth": 1})


class ObservationUnitController(BaseController[ObservationUnit]):
    path = "/observation_unit"
    dto = ObservationUnitDTO.write_dto
    return_dto = ObservationUnitDTO.read_dto
