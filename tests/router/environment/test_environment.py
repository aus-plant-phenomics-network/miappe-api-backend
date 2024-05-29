from dataclasses import dataclass
from uuid import UUID

from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.environment import Environment, EnvironmentDataclass
from tests.helpers import validate_post, validate_put
from tests.router.environment.fixture import (
    BARLEY_FERTILIZER,
    BARLEY_LIGHT_INTENSITY,
    BARLEY_RELATIVE_HUMIDITY,
    BARLEY_ROOTING_MEDIUM,
    BARLEY_SOWING_DENSITY,
    BARLEY_TEMPERATURE,
    BARLEY_WATERING_EXPOSURE,
    MAIZE_PH,
    MAIZE_ROOTING_MEDIUM,
    MAIZE_SOWING_DENSITY,
    PATH,
    AllEnvironmentFixtureResponse,
    EnvironmentResponse,
)


@dataclass
class EnvironmentFixture:
    id: UUID
    response: Response
    data: EnvironmentDataclass
    study_id: list[UUID]


def get_environment_fixture(response: EnvironmentResponse, data: Environment) -> EnvironmentFixture:
    environment_response = response.environment_response
    study_id = [item.json()["id"] for item in response.study_response]
    fixture = EnvironmentDataclass(study_id=study_id, **data.to_dict())
    return EnvironmentFixture(
        id=environment_response.json()["id"], response=environment_response, data=fixture, study_id=study_id
    )


async def test_all_environments_created(
    setup_environment: AllEnvironmentFixtureResponse, test_client: AsyncTestClient
) -> None:
    fixture = get_environment_fixture(setup_environment.maize_sowing_density, MAIZE_SOWING_DENSITY)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_environment_fixture(setup_environment.maize_rooting_medium, MAIZE_ROOTING_MEDIUM)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_environment_fixture(setup_environment.maize_ph, MAIZE_PH)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_environment_fixture(setup_environment.barley_fertilizer, BARLEY_FERTILIZER)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_environment_fixture(setup_environment.barley_light_intensity, BARLEY_LIGHT_INTENSITY)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_environment_fixture(setup_environment.barley_temperature, BARLEY_TEMPERATURE)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_environment_fixture(setup_environment.barley_watering_exposure, BARLEY_WATERING_EXPOSURE)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_environment_fixture(setup_environment.barley_sowing_density, BARLEY_SOWING_DENSITY)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_environment_fixture(setup_environment.barley_rooting_medium, BARLEY_ROOTING_MEDIUM)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_environment_fixture(setup_environment.barley_relative_humidity, BARLEY_RELATIVE_HUMIDITY)
    await validate_post(PATH, fixture.data, test_client, fixture.response)


async def test_environment_file_updated(
    update_environment: AllEnvironmentFixtureResponse, test_client: AsyncTestClient
) -> None:
    fixture = get_environment_fixture(update_environment.maize_sowing_density, MAIZE_SOWING_DENSITY)
    await validate_put(PATH, fixture.data, test_client, fixture.response)
