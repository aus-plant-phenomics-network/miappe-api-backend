from src.model import Experiment
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("ExperimentController",)


ExperimentDTO = DTOGenerator[Experiment]()


class ExperimentController(BaseController[Experiment]):
    path = "/experiment"
    dto = ExperimentDTO.write_dto
    return_dto = ExperimentDTO.read_dto
