from litestar.dto import DataclassDTO, DTOConfig

from src.model.data_file import DataFile, DataFileDataclass
from src.model.study import Study
from src.router.base import DataclassController
from src.router.utils.dto import DTOGenerator

__all__ = ("DataFileController",)


class DataFileDTO(DataclassDTO[DataFileDataclass]):
    config = DTOConfig(rename_strategy="camel")


DataFileReturnDTO = DTOGenerator[DataFile]()


class DataFileController(DataclassController[DataFile, DataFileDataclass]):
    path = "/dataFile"
    dto = DataFileDTO
    return_dto = DataFileDTO
    attr_map = {"studies": ("study_id", Study)}
    selectinload_attrs = [DataFile.studies]
