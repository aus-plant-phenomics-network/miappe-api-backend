# from typing import TYPE_CHECKING

# from src.model import Institution
# from src.router.base import BaseController
# from src.router.utils.dto import DTOGenerator

# __all__ = ("InstitutionController",)

# if TYPE_CHECKING:
#     pass

# InstitutionDTO = DTOGenerator[Institution](read_kwargs={"max_nested_depth": 1})


# class InstitutionController(BaseController[Institution]):
#     path = "/institution"
#     dto = InstitutionDTO.write_dto
#     return_dto = InstitutionDTO.read_dto
