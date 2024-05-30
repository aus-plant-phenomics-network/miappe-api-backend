from litestar.dto import DataclassDTO, DTOConfig

from src.model.environment import Environment, EnvironmentDataclass
from src.model.study import Study
from src.router.base import DataclassController
from src.router.utils.dto import DTOGenerator

__all__ = ("EnvironmentController",)


class EnvironmentDTO(DataclassDTO[EnvironmentDataclass]):
    config = DTOConfig(rename_strategy="camel")


EnvironmentReturnDTO = DTOGenerator[Environment]()


class EnvironmentController(DataclassController[Environment, EnvironmentDataclass]):
    path = "/environment"
    dto = EnvironmentDTO
    return_dto = EnvironmentDTO
    attr_map = {"studies": ("study_id", Study)}
    selectinload_attrs = [Environment.studies]
