from src.model import ExperimentalFactor
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("ExperimentalFactorController",)


ExperimentalFactorDTO = DTOGenerator[ExperimentalFactor](read_kwargs={"max_nested_depth": 1})


class ExperimentalFactorController(BaseController[ExperimentalFactor]):
    path = "/experimental_factor"
    dto = ExperimentalFactorDTO.write_dto
    return_dto = ExperimentalFactorDTO.read_dto
