from typing import TYPE_CHECKING

from src.model import Event
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("EventController",)

if TYPE_CHECKING:
    pass

EventDTO = DTOGenerator[Event](read_kwargs={"max_nested_depth": 1})


class EventController(BaseController[Event]):
    path = "/event"
    dto = EventDTO.write_dto
    return_dto = EventDTO.read_dto
