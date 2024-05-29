from collections.abc import AsyncGenerator
from dataclasses import dataclass
from uuid import UUID

import pytest
from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.environment import Environment, EnvironmentDataclass
from tests.helpers import delete_fixture, post_fixture, put_fixture
from tests.router.study.fixture import AllStudyFixtureResponse


@dataclass
class EnvironmentResponse:
    environment_response: Response
    study_response: list[Response]


@dataclass
class AllEnvironmentFixtureResponse:
    maize_sowing_density: EnvironmentResponse
    maize_rooting_medium: EnvironmentResponse
    maize_ph: EnvironmentResponse
    barley_sowing_density: EnvironmentResponse
    barley_rooting_medium: EnvironmentResponse
    barley_fertilizer: EnvironmentResponse
    barley_watering_exposure: EnvironmentResponse
    barley_light_intensity: EnvironmentResponse
    barley_relative_humidity: EnvironmentResponse
    barley_temperature: EnvironmentResponse
    study_response: AllStudyFixtureResponse


PATH = "environment"
MAIZE_SOWING_DENSITY = Environment(
    parameter="sowing density", setpoint="300 seeds per m2", description="maize expermiment environment variable"
)
MAIZE_ROOTING_MEDIUM = Environment(
    parameter="rooting medium composition",
    setpoint="50% clay plus sand",
    description="maize expermiment environment variable",
)
MAIZE_PH = Environment(parameter="pH", setpoint="6.5", description="maize expermiment environment variable")
BARLEY_SOWING_DENSITY = Environment(
    parameter="sowing density", setpoint="1 plant per 150mm pots", description="barley expermiment environment variable"
)
BARLEY_ROOTING_MEDIUM = Environment(
    parameter="rooting medium composition",
    setpoint="1:9 autoclaved Arboretum soil/autoclaved play sand with or without mycorrhizal inoculum",
    description="barley expermiment environment variable",
)
BARLEY_FERTILIZER = Environment(
    parameter="fertilizer",
    setpoint="1/2 strength Long-Ashton Zn P (given once per week at rate of approx. 20mL) once weekly",
    description="barley expermiment environment variable",
)
BARLEY_WATERING_EXPOSURE = Environment(
    parameter="watering exposure", setpoint="daily", description="barley expermiment environment variable"
)
BARLEY_LIGHT_INTENSITY = Environment(
    parameter="light intensity",
    setpoint="hourly light intensity measurement of the greenhouse",
    description="barley expermiment environment variable",
)
BARLEY_RELATIVE_HUMIDITY = Environment(
    parameter="relative humidity",
    setpoint="hourly relative humidity measurement of the greenhouse",
    description="barley expermiment environment variable",
)
BARLEY_TEMPERATURE = Environment(
    parameter="temperature",
    setpoint="hourly temperature measurement of the greenhouse",
    description="barley expermiment environment variable",
)


async def get_environment_fixture(
    data: Environment, studies: list[Response], test_client: AsyncTestClient, id: UUID | None = None
) -> EnvironmentResponse:
    study_id = [item.json()["id"] for item in studies]
    send_data = EnvironmentDataclass(study_id=study_id, **data.to_dict())
    if id is None:
        send_data.updated_at = None
        response = await post_fixture(PATH, send_data, test_client)
    else:
        response = await put_fixture(PATH, send_data, test_client, id)
    return EnvironmentResponse(study_response=studies, environment_response=response)


@pytest.fixture(scope="function")
async def setup_environment(
    setup_study: AllStudyFixtureResponse, test_client: AsyncTestClient
) -> AsyncGenerator[AllEnvironmentFixtureResponse, None]:
    maize_study = setup_study.maize.study_response
    barley_study = setup_study.barley.study_response
    maize_sowing_density = await get_environment_fixture(MAIZE_SOWING_DENSITY, [maize_study, barley_study], test_client)
    maize_rooting_medium = await get_environment_fixture(MAIZE_ROOTING_MEDIUM, [maize_study], test_client)
    maize_ph = await get_environment_fixture(MAIZE_PH, [maize_study], test_client)
    barley_sowing_density = await get_environment_fixture(BARLEY_SOWING_DENSITY, [barley_study], test_client)
    barley_rooting_medium = await get_environment_fixture(BARLEY_ROOTING_MEDIUM, [barley_study], test_client)
    barley_ferterlizer = await get_environment_fixture(BARLEY_FERTILIZER, [barley_study], test_client)
    barley_watering_exposure = await get_environment_fixture(BARLEY_WATERING_EXPOSURE, [barley_study], test_client)
    barley_light_intensity = await get_environment_fixture(BARLEY_LIGHT_INTENSITY, [barley_study], test_client)
    barley_relative_humidity = await get_environment_fixture(BARLEY_RELATIVE_HUMIDITY, [barley_study], test_client)
    barley_temperature = await get_environment_fixture(BARLEY_TEMPERATURE, [barley_study], test_client)

    yield AllEnvironmentFixtureResponse(
        maize_sowing_density=maize_sowing_density,
        maize_rooting_medium=maize_rooting_medium,
        maize_ph=maize_ph,
        barley_sowing_density=barley_sowing_density,
        barley_rooting_medium=barley_rooting_medium,
        barley_fertilizer=barley_ferterlizer,
        barley_watering_exposure=barley_watering_exposure,
        barley_light_intensity=barley_light_intensity,
        barley_relative_humidity=barley_relative_humidity,
        barley_temperature=barley_temperature,
        study_response=setup_study,
    )
    await delete_fixture(PATH, maize_sowing_density.environment_response.json()["id"], test_client)
    await delete_fixture(PATH, maize_rooting_medium.environment_response.json()["id"], test_client)
    await delete_fixture(PATH, maize_ph.environment_response.json()["id"], test_client)
    await delete_fixture(PATH, barley_sowing_density.environment_response.json()["id"], test_client)
    await delete_fixture(PATH, barley_rooting_medium.environment_response.json()["id"], test_client)
    await delete_fixture(PATH, barley_ferterlizer.environment_response.json()["id"], test_client)
    await delete_fixture(PATH, barley_watering_exposure.environment_response.json()["id"], test_client)
    await delete_fixture(PATH, barley_light_intensity.environment_response.json()["id"], test_client)
    await delete_fixture(PATH, barley_relative_humidity.environment_response.json()["id"], test_client)
    await delete_fixture(PATH, barley_temperature.environment_response.json()["id"], test_client)


@pytest.fixture(scope="function")
async def update_environment(
    setup_environment: AllEnvironmentFixtureResponse, test_client: AsyncTestClient
) -> AsyncGenerator[AllEnvironmentFixtureResponse, None]:
    all_responses = setup_environment
    maize_study = all_responses.study_response.maize.study_response
    maize_sowing_density = all_responses.maize_sowing_density
    maize_sowing_density_response = await get_environment_fixture(
        MAIZE_SOWING_DENSITY, [maize_study], test_client, maize_sowing_density.environment_response.json()["id"]
    )
    all_responses.maize_sowing_density = maize_sowing_density_response
    yield all_responses
