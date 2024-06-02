from dataclasses import dataclass
from uuid import UUID

from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.event import Event, EventDataclass
from tests.helpers import validate_post, validate_put
from tests.router.event.fixture import (
    FERTILIZING_EVENT,
    PATH,
    PLANTING_EVENT,
    WATERING_EVENT,
    AllEventFixtureResponse,
    EventResponse,
)


@dataclass
class EventFixture:
    id: UUID
    response: Response
    data: EventDataclass
    event_type_id: UUID
    study_id: list[UUID]
    observation_unit_id: list[UUID]


def get_event_fixture(response: EventResponse, data: Event) -> EventFixture:
    event_response = response.event_response
    study_id = [item.json()["id"] for item in response.study_response]
    event_type_id = response.event_type.json()["id"]
    observation_unit_id = [item.json()["id"] for item in response.observation_unit_response]
    fixture = EventDataclass(
        study_id=study_id, event_type_id=event_type_id, observation_unit_id=observation_unit_id, **data.to_dict()
    )
    return EventFixture(
        id=event_response.json()["id"],
        response=event_response,
        data=fixture,
        study_id=study_id,
        event_type_id=event_type_id,
        observation_unit_id=observation_unit_id,
    )


async def test_all_events_created(setup_event: AllEventFixtureResponse, test_client: AsyncTestClient) -> None:
    fixture = get_event_fixture(setup_event.fertilizing, FERTILIZING_EVENT)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_event_fixture(setup_event.planting, PLANTING_EVENT)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_event_fixture(setup_event.watering, WATERING_EVENT)
    await validate_post(PATH, fixture.data, test_client, fixture.response)


async def test_event_file_updated(update_event: AllEventFixtureResponse, test_client: AsyncTestClient) -> None:
    fixture = get_event_fixture(update_event.planting, PLANTING_EVENT)
    await validate_put(PATH, fixture.data, test_client, fixture.response)
