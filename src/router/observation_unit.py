from litestar.dto import DataclassDTO, DTOConfig

from src.model.experimental_factor import ExperimentalFactor
from src.model.observation_unit import ObservationUnit, ObservationUnitDataclass
from src.model.study import Study
from src.router.base import DataclassController
from src.router.utils.dto import DTOGenerator

__all__ = ("ObservationUnitController",)


class ObservationUnitDTO(DataclassDTO[ObservationUnitDataclass]):
    config = DTOConfig(rename_strategy="camel")


ObservationUnitReturnDTO = DTOGenerator[ObservationUnit]()


class ObservationUnitController(DataclassController[ObservationUnit, ObservationUnitDataclass]):
    path = "/observationUnit"
    dto = ObservationUnitDTO
    return_dto = ObservationUnitDTO
    attr_map = {
        "parents": ("parent_id", ObservationUnit),
        "studies": ("study_id", Study),
        "experimental_factors": ("experimental_factor_id", ExperimentalFactor),
    }
    selectinload_attrs = [ObservationUnit.parents, ObservationUnit.studies, ObservationUnit.experimental_factors]
