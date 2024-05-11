# from typing import TYPE_CHECKING

# from src.model import BiologicalMaterial
# from src.router.base import BaseController
# from src.router.utils.dto import DTOGenerator

# __all__ = ("BiologicalMaterialController",)

# if TYPE_CHECKING:
#     pass

# BiologicalMaterialDTO = DTOGenerator[BiologicalMaterial](read_kwargs={"max_nested_depth": 1})


# class BiologicalMaterialController(BaseController[BiologicalMaterial]):
#     path = "/biological_material"
#     dto = BiologicalMaterialDTO.write_dto
#     return_dto = BiologicalMaterialDTO.read_dto
