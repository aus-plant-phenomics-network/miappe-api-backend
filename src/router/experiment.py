from litestar.dto import DataclassDTO, DTOConfig

from src.model.experiment import Experiment, ExperimentDataclass
from src.model.facility import Facility
from src.model.staff import Staff
from src.router.base import DataclassController
from src.router.utils.dto import DTOGenerator

__all__ = ("ExperimentController",)


class ExperimentDTO(DataclassDTO[ExperimentDataclass]):
    config = DTOConfig(rename_strategy="camel")


ExperimentReturnDTO = DTOGenerator[Experiment]()


class ExperimentController(DataclassController[Experiment, ExperimentDataclass]):
    path = "/experiment"
    dto = ExperimentDTO
    return_dto = ExperimentDTO
    attr_map = {"facilities": ("facility_id", Facility), "staffs": ("staff_id", Staff)}
    selectinload_attrs = [Experiment.facilities, Experiment.staffs]
