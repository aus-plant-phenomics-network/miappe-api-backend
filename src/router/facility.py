from typing import TYPE_CHECKING

from src.model import Facility
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("FacilityController",)

if TYPE_CHECKING:
    pass

FacilityDTO = DTOGenerator[Facility](read_kwargs={"max_nested_depth": 1})


class FacilityController(BaseController[Facility]):
    path = "/facility"
    dto = FacilityDTO.write_dto
    return_dto = FacilityDTO.read_dto
