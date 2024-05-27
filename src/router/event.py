from src.model import Event
from src.router.base import BaseController
from src.router.utils.dto import DTOGenerator

__all__ = ("EventController",)


EventDTO = DTOGenerator[Event]()


class EventController(BaseController[Event]):
    path = "/event"
    dto = EventDTO.write_dto
    return_dto = EventDTO.read_dto
