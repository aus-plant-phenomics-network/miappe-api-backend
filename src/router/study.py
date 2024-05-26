from src.model import Study
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("StudyController",)


StudyDTO = DTOGenerator[Study]()


class StudyController(BaseController[Study]):
    path = "/study"
    dto = StudyDTO.write_dto
    return_dto = StudyDTO.read_dto
