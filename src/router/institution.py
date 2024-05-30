from litestar.dto import DataclassDTO, DTOConfig

from src.model.institution import Institution, InstitutionDataclass
from src.router.base import DataclassController
from src.router.utils.dto import DTOGenerator

__all__ = ("InstitutionController",)


class InstitutionDTO(DataclassDTO[InstitutionDataclass]):
    config = DTOConfig(rename_strategy="camel")


InstitutionReturnDTO = DTOGenerator[Institution]()


class InstitutionController(DataclassController[Institution, InstitutionDataclass]):
    path = "/institution"
    dto = InstitutionDTO
    return_dto = InstitutionDTO
    attr_map = {"parents": ("parent_id", Institution)}
    selectinload_attrs = [Institution.parents]
