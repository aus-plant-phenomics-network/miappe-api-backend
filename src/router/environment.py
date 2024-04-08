from typing import TYPE_CHECKING

from src.model import Environment
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("EnvironmentController",)

if TYPE_CHECKING:
    pass

EnvironmentDTO = DTOGenerator[Environment](read_kwargs={"max_nested_depth": 1})


class EnvironmentController(BaseController[Environment]):
    path = "/environment"
    dto = EnvironmentDTO.write_dto
    return_dto = EnvironmentDTO.read_dto
