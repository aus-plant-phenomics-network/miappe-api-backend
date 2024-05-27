from src.model import Facility
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("FacilityController",)


FacilityDTO = DTOGenerator[Facility]()


class FacilityController(BaseController[Facility]):
    path = "/facility"
    dto = FacilityDTO.write_dto
    return_dto = FacilityDTO.read_dto
