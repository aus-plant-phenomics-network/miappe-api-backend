import datetime
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from uuid import UUID

import pytest
from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.event import Event, EventDataclass
from src.model.vocabulary import Vocabulary
from tests.helpers import delete_fixture, post_fixture, put_fixture
from tests.router.observation_unit.fixture import AllObservationUnitFixtureResponse
from tests.router.study.fixture import AllStudyFixtureResponse


@dataclass
class EventTypeResponse:
    planting: Response
    fertilizing: Response
    watering: Response


@dataclass
class EventResponse:
    event_response: Response
    event_type: Response
    study_response: list[Response]
    observation_unit_response: list[Response]


@dataclass
class AllEventFixtureResponse:
    planting: EventResponse
    fertilizing: EventResponse
    watering: EventResponse
    event_type: EventTypeResponse
    studies: AllStudyFixtureResponse
    observation_units: AllObservationUnitFixtureResponse


PATH = "event"
PLANTING_TYPE = Vocabulary(title="Planting", accession_number="CO_715:0000007")
PLANTING_EVENT = Event(
    title="Planting Seed - Maize Experiment",
    description="Sowing using seed drill",
    event_date=datetime.datetime(2006, 9, 27),
)

FERTILIZING_TYPE = Vocabulary(title="Fertilizing", accession_number="CO_715:0000011")
FERTILIZING_EVENT = Event(
    title="Fertilizing - Maize Experiment",
    description="Fertilizer application: Ammonium nitrate at 3 kg/m2",
    event_date=datetime.datetime(2006, 10, 27),
)

WATERING_TYPE = Vocabulary(title="Watering Exposure", accession_number="PECO:0007383")
WATERING_EVENT = Event(
    title="Watering - Barley Experiment",
    description="Automated pot weight based watering regime during experiment",
    event_date=datetime.datetime(2017, 4, 6),
)


async def get_event_fixture(
    data: Event,
    event_type: Response,
    studies: list[Response],
    observation_units: list[Response],
    test_client: AsyncTestClient,
    id: UUID | None = None,
) -> EventResponse:
    study_id = [item.json()["id"] for item in studies]
    observation_unit_id = [item.json()["id"] for item in observation_units]
    event_type_id = event_type.json()["id"]
    send_data = EventDataclass(
        study_id=study_id,
        observation_unit_id=observation_unit_id,
        event_type_id=event_type_id,
        **data.to_dict(),
    )
    if id is None:
        send_data.updated_at = None
        response = await post_fixture(PATH, send_data, test_client)
    else:
        response = await put_fixture(PATH, send_data, test_client, id)
    return EventResponse(
        study_response=studies,
        event_response=response,
        event_type=event_type,
        observation_unit_response=observation_units,
    )


@pytest.fixture(scope="function")
async def setup_event_type(test_client: AsyncTestClient) -> AsyncGenerator[EventTypeResponse, None]:
    planting = await post_fixture("vocabulary", PLANTING_TYPE, test_client)
    fertlizing = await post_fixture("vocabulary", FERTILIZING_TYPE, test_client)
    watering = await post_fixture("vocabulary", WATERING_TYPE, test_client)
    yield EventTypeResponse(planting=planting, fertilizing=fertlizing, watering=watering)
    await delete_fixture("vocabulary", planting.json()["id"], test_client)
    await delete_fixture("vocabulary", fertlizing.json()["id"], test_client)
    await delete_fixture("vocabulary", watering.json()["id"], test_client)


@pytest.fixture(scope="function")
async def setup_event(
    setup_event_type: EventTypeResponse,
    setup_study: AllStudyFixtureResponse,
    setup_observation_units: AllObservationUnitFixtureResponse,
    test_client: AsyncTestClient,
) -> AsyncGenerator[AllEventFixtureResponse, None]:
    maize_study = setup_study.maize.study_response
    barley_study = setup_study.barley.study_response

    planting = setup_event_type.planting
    fertilizing = setup_event_type.fertilizing
    watering = setup_event_type.fertilizing

    plot_894 = setup_observation_units.plot_894.observation_unit_response
    plant_061439 = setup_observation_units.plant_061439.observation_unit_response
    plant_061440 = setup_observation_units.plant_061440.observation_unit_response

    planting_event = await get_event_fixture(
        PLANTING_EVENT, planting, [maize_study, barley_study], [plot_894], test_client
    )
    fertilizing_event = await get_event_fixture(FERTILIZING_EVENT, fertilizing, [maize_study], [plot_894], test_client)
    watering_event = await get_event_fixture(
        WATERING_EVENT, watering, [barley_study], [plant_061439, plant_061440], test_client
    )

    yield AllEventFixtureResponse(
        planting=planting_event,
        fertilizing=fertilizing_event,
        watering=watering_event,
        event_type=setup_event_type,
        studies=setup_study,
        observation_units=setup_observation_units,
    )
    await delete_fixture(PATH, planting_event.event_response.json()["id"], test_client)
    await delete_fixture(PATH, fertilizing_event.event_response.json()["id"], test_client)
    await delete_fixture(PATH, watering_event.event_response.json()["id"], test_client)


@pytest.fixture(scope="function")
async def update_event(
    setup_event: AllEventFixtureResponse, test_client: AsyncTestClient
) -> AsyncGenerator[AllEventFixtureResponse, None]:
    all_responses = setup_event
    maize_study = all_responses.studies.maize.study_response
    planting_id = all_responses.planting.event_response.json()["id"]
    planting = await get_event_fixture(
        PLANTING_EVENT,
        event_type=all_responses.event_type.planting,
        studies=[maize_study],
        observation_units=[all_responses.observation_units.plot_894.observation_unit_response],
        test_client=test_client,
        id=planting_id,
    )
    all_responses.planting = planting
    yield all_responses
