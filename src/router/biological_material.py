from litestar.dto import DataclassDTO, DTOConfig

from src.model.biological_material import BiologicalMaterial, BiologicalMaterialDataclass
from src.model.study import Study
from src.router.base import DataclassController
from src.router.utils.dto import DTOGenerator

__all__ = ("BiologicalMaterialController",)


class BiologicalMaterialDTO(DataclassDTO[BiologicalMaterialDataclass]):
    config = DTOConfig(rename_strategy="camel")


BiologicalMaterialReturnDTO = DTOGenerator[BiologicalMaterial]()


class BiologicalMaterialController(DataclassController[BiologicalMaterial, BiologicalMaterialDataclass]):
    path = "/biologicalMaterial"
    dto = BiologicalMaterialDTO
    return_dto = BiologicalMaterialDTO
    attr_map = {"studies": ("study_id", Study)}
    selectinload_attrs = [BiologicalMaterial.studies]
