from litestar.dto import DataclassDTO, DTOConfig

from src.model.event import Event, EventDataclass
from src.model.observation_unit import ObservationUnit
from src.model.study import Study
from src.router.base import DataclassController
from src.router.utils.dto import DTOGenerator

__all__ = ("EventController",)


class EventDTO(DataclassDTO[EventDataclass]):
    config = DTOConfig(rename_strategy="camel")


EventReturnDTO = DTOGenerator[Event]()


class EventController(DataclassController[Event, EventDataclass]):
    path = "/event"
    dto = EventDTO
    return_dto = EventDTO
    attr_map = {
        "studies": ("study_id", Study),
        "observation_units": ("observation_unit_id", ObservationUnit),
    }
    selectinload_attrs = [Event.studies, Event.observation_units]
