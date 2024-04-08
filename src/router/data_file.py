from typing import TYPE_CHECKING

from src.model import DataFile
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("DataFileController",)

if TYPE_CHECKING:
    pass

DataFileDTO = DTOGenerator[DataFile](read_kwargs={"max_nested_depth": 1})


class DataFileController(BaseController[DataFile]):
    path = "/data_file"
    dto = DataFileDTO.write_dto
    return_dto = DataFileDTO.read_dto
