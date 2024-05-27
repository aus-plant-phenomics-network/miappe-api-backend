from src.model import ObservationUnit
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("ObservationUnitController",)


ObservationUnitDTO = DTOGenerator[ObservationUnit]()


class ObservationUnitController(BaseController[ObservationUnit]):
    path = "/observation_unit"
    dto = ObservationUnitDTO.write_dto
    return_dto = ObservationUnitDTO.read_dto
