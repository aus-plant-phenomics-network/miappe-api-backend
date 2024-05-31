from litestar.dto import DataclassDTO, DTOConfig

from src.model.observed_variable import ObservedVariable, ObservedVariableDataclass
from src.model.study import Study
from src.router.base import DataclassController
from src.router.utils.dto import DTOGenerator

__all__ = ("ObservedVariableController",)


class ObservedVariableDTO(DataclassDTO[ObservedVariableDataclass]):
    config = DTOConfig(rename_strategy="camel")


ObservedVariableReturnDTO = DTOGenerator[ObservedVariable]()


class ObservedVariableController(DataclassController[ObservedVariable, ObservedVariableDataclass]):
    path = "/observedVariable"
    dto = ObservedVariableDTO
    return_dto = ObservedVariableDTO
    attr_map = {"studies": ("study_id", Study)}
    selectinload_attrs = [ObservedVariable.studies]
