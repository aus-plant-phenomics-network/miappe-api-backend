from collections.abc import AsyncGenerator
from dataclasses import dataclass
from uuid import UUID

import pytest
from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.observed_variable import ObservedVariable, ObservedVariableDataclass
from src.model.vocabulary import Vocabulary
from tests.helpers import delete_fixture, post_fixture, put_fixture
from tests.router.study.fixture import AllStudyFixtureResponse


@dataclass
class ObservedVariableResponse:
    observed_variable_response: Response
    study_response: list[Response]


@dataclass
class AllObservedVariableFixtureResponse:
    projected_shoot_area: ObservedVariableResponse
    zn_concentration: ObservedVariableResponse


@dataclass
class VariableReferenceResponse:
    anthesis: Response


@dataclass
class VariableTraitResponse:
    anthesis: Response
    reproductive_growth_time: Response
    projected_shoot_area: Response
    zn_concentration: Response


PATH = "observed_variable"
ANTHESIS_TRAIT = Vocabulary(title="Anthesis time", accession_number="CO_322:0000030")
REPRODUCTIVE_GROWTH_TIME_TRAIT = Vocabulary(title="Reproductive growth time", accession_number="TO:0000366")
PROJECTED_SHOOT_AREA_TRAIT = Vocabulary(title="Projected shoot area")
ZN_CONCENTRATION_TRAIT = Vocabulary(title="Zn concentration", accession_number="CDNO_0200170")

ANTHESIS_VARIABLE = ObservedVariable(title="Ant_Cmp_Cday", description="Anthesis computed in growing degree days")
PROJECTED_SHOOT_AREA_VARIABLE = ObservedVariable(title="PSA_img_kpixels")
ZN_CONCENTRATION_VARIABLE = ObservedVariable(title="Zn_conc")


async def get_observed_variable_fixture(
    data: ObservedVariable, studies: list[Response], test_client: AsyncTestClient, id: UUID | None = None
) -> ObservedVariableResponse:
    study_id = [item.json()["id"] for item in studies]
    send_data = ObservedVariableDataclass(study_id=study_id, **data.to_dict())
    if id is None:
        send_data.updated_at = None
        response = await post_fixture(PATH, send_data, test_client)
    else:
        response = await put_fixture(PATH, send_data, test_client, id)
    return ObservedVariableResponse(study_response=studies, observed_variable_response=response)


@pytest.fixture(scope="function")
async def setup_observed_variable(
    setup_study: AllStudyFixtureResponse, test_client: AsyncTestClient
) -> AsyncGenerator[AllObservedVariableFixtureResponse, None]:
    maize_study = setup_study.maize.study_response
    barley_study = setup_study.barley.study_response
    maize_sowing_density = await get_observed_variable_fixture(
        MAIZE_SOWING_DENSITY, [maize_study, barley_study], test_client
    )
    maize_rooting_medium = await get_observed_variable_fixture(MAIZE_ROOTING_MEDIUM, [maize_study], test_client)
    maize_ph = await get_observed_variable_fixture(MAIZE_PH, [maize_study], test_client)
    barley_sowing_density = await get_observed_variable_fixture(BARLEY_SOWING_DENSITY, [barley_study], test_client)
    barley_rooting_medium = await get_observed_variable_fixture(BARLEY_ROOTING_MEDIUM, [barley_study], test_client)
    barley_ferterlizer = await get_observed_variable_fixture(BARLEY_FERTILIZER, [barley_study], test_client)
    barley_watering_exposure = await get_observed_variable_fixture(
        BARLEY_WATERING_EXPOSURE, [barley_study], test_client
    )
    barley_light_intensity = await get_observed_variable_fixture(BARLEY_LIGHT_INTENSITY, [barley_study], test_client)
    barley_relative_humidity = await get_observed_variable_fixture(
        BARLEY_RELATIVE_HUMIDITY, [barley_study], test_client
    )
    barley_temperature = await get_observed_variable_fixture(BARLEY_TEMPERATURE, [barley_study], test_client)

    yield AllObservedVariableFixtureResponse(
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
    await delete_fixture(PATH, maize_sowing_density.observed_variable_response.json()["id"], test_client)
    await delete_fixture(PATH, maize_rooting_medium.observed_variable_response.json()["id"], test_client)
    await delete_fixture(PATH, maize_ph.observed_variable_response.json()["id"], test_client)
    await delete_fixture(PATH, barley_sowing_density.observed_variable_response.json()["id"], test_client)
    await delete_fixture(PATH, barley_rooting_medium.observed_variable_response.json()["id"], test_client)
    await delete_fixture(PATH, barley_ferterlizer.observed_variable_response.json()["id"], test_client)
    await delete_fixture(PATH, barley_watering_exposure.observed_variable_response.json()["id"], test_client)
    await delete_fixture(PATH, barley_light_intensity.observed_variable_response.json()["id"], test_client)
    await delete_fixture(PATH, barley_relative_humidity.observed_variable_response.json()["id"], test_client)
    await delete_fixture(PATH, barley_temperature.observed_variable_response.json()["id"], test_client)


@pytest.fixture(scope="function")
async def update_observed_variable(
    setup_observed_variable: AllObservedVariableFixtureResponse, test_client: AsyncTestClient
) -> AsyncGenerator[AllObservedVariableFixtureResponse, None]:
    all_responses = setup_observed_variable
    maize_study = all_responses.study_response.maize.study_response
    maize_sowing_density = all_responses.maize_sowing_density
    maize_sowing_density_response = await get_observed_variable_fixture(
        MAIZE_SOWING_DENSITY, [maize_study], test_client, maize_sowing_density.observed_variable_response.json()["id"]
    )
    all_responses.maize_sowing_density = maize_sowing_density_response
    yield all_responses
