from typing import TYPE_CHECKING

from src.model import Study
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("StudyController",)

if TYPE_CHECKING:
    pass

StudyDTO = DTOGenerator[Study](read_kwargs={"max_nested_depth": 1})


class StudyController(BaseController[Study]):
    path = "/study"
    dto = StudyDTO.write_dto
    return_dto = StudyDTO.read_dto
