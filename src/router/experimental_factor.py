from litestar.dto import DataclassDTO, DTOConfig

from src.model.experimental_factor import ExperimentalFactor, ExperimentalFactorDataclass
from src.model.study import Study
from src.router.base import DataclassController
from src.router.utils.dto import DTOGenerator

__all__ = ("ExperimentalFactorController",)


class ExperimentalFactorDTO(DataclassDTO[ExperimentalFactorDataclass]):
    config = DTOConfig(rename_strategy="camel")


ExperimentalFactorReturnDTO = DTOGenerator[ExperimentalFactor]()


class ExperimentalFactorController(DataclassController[ExperimentalFactor, ExperimentalFactorDataclass]):
    path = "/experimentalFactor"
    dto = ExperimentalFactorDTO
    return_dto = ExperimentalFactorDTO
    attr_map = {"studies": ("study_id", Study)}
    selectinload_attrs = [ExperimentalFactor.studies]
