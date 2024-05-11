# from typing import TYPE_CHECKING

# from src.model import Experiment
# from src.router.base import BaseController
# from src.router.utils.dto import DTOGenerator

# __all__ = ("ExperimentController",)

# if TYPE_CHECKING:
#     pass

# ExperimentDTO = DTOGenerator[Experiment](read_kwargs={"max_nested_depth": 1})


# class ExperimentController(BaseController[Experiment]):
#     path = "/experiment"
#     dto = ExperimentDTO.write_dto
#     return_dto = ExperimentDTO.read_dto
