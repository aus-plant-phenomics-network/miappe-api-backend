from src.model import Sample
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("SampleController",)


SampleDTO = DTOGenerator[Sample]()


class SampleController(BaseController[Sample]):
    path = "/sample"
    dto = SampleDTO.write_dto
    return_dto = SampleDTO.read_dto
