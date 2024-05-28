from src.model import Method
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("MethodController",)


MethodDTO = DTOGenerator[Method]()


class MethodController(BaseController[Method]):
    path = "/method"
    dto = MethodDTO.read_dto
    return_dto = MethodDTO.write_dto
