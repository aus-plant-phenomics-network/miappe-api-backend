from typing import TYPE_CHECKING

from src.model import Sample
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("SampleController",)

if TYPE_CHECKING:
    pass

SampleDTO = DTOGenerator[Sample](read_kwargs={"max_nested_depth": 1})


class SampleController(BaseController[Sample]):
    path = "/sample"
    dto = SampleDTO.write_dto
    return_dto = SampleDTO.read_dto
