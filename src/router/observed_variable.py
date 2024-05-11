# from typing import TYPE_CHECKING

# from src.model import ObservedVariable
# from src.router.base import BaseController
# from src.router.utils.dto import DTOGenerator

# __all__ = ("ObservedVariableController",)

# if TYPE_CHECKING:
#     pass

# ObservedVariableDTO = DTOGenerator[ObservedVariable](read_kwargs={"max_nested_depth": 1})


# class ObservedVariableController(BaseController[ObservedVariable]):
#     path = "/observed_variable"
#     dto = ObservedVariableDTO.write_dto
#     return_dto = ObservedVariableDTO.read_dto
