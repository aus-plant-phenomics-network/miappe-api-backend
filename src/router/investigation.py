from src.model import Investigation
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("InvestigationController",)


InvestigationDTO = DTOGenerator[Investigation]()


class InvestigationController(BaseController[Investigation, Investigation, Investigation]):
    path = "/investigation"
    dto = InvestigationDTO.write_dto
    return_dto = InvestigationDTO.read_dto
