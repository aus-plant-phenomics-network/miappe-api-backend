from src.model import Environment
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("EnvironmentController",)


EnvironmentDTO = DTOGenerator[Environment]()


class EnvironmentController(BaseController[Environment]):
    path = "/environment"
    dto = EnvironmentDTO.write_dto
    return_dto = EnvironmentDTO.read_dto
