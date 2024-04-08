from typing import TYPE_CHECKING

from src.model import Investigation
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("InvestigationController",)

if TYPE_CHECKING:
    pass

InvestigationDTO = DTOGenerator[Investigation](read_kwargs={"max_nested_depth": 1})


class InvestigationController(BaseController[Investigation]):
    path = "/investigation"
    dto = InvestigationDTO.write_dto
    return_dto = InvestigationDTO.read_dto
