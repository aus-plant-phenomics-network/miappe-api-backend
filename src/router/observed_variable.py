from src.model import ObservedVariable
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("ObservedVariableController",)


ObservedVariableDTO = DTOGenerator[ObservedVariable]()


class ObservedVariableController(BaseController[ObservedVariable]):
    path = "/observedVariable"
    dto = ObservedVariableDTO.write_dto
    return_dto = ObservedVariableDTO.read_dto
