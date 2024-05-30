from litestar.dto import DataclassDTO, DTOConfig

from src.model.institution import Institution
from src.model.staff import Staff, StaffDataclass
from src.router.base import DataclassController
from src.router.utils.dto import DTOGenerator

__all__ = ("StaffController",)


class StaffDTO(DataclassDTO[StaffDataclass]):
    config = DTOConfig(rename_strategy="camel")


StaffReturnDTO = DTOGenerator[Staff]()


class StaffController(DataclassController[Staff, StaffDataclass]):
    path = "/staff"
    dto = StaffDTO
    return_dto = StaffDTO
    attr_map = {"institutions": ("institution_id", Institution)}
    selectinload_attrs = [Staff.institutions]
