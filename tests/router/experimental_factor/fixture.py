from collections.abc import AsyncGenerator
from dataclasses import dataclass
from uuid import UUID

import pytest
from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.experimental_factor import ExperimentalFactor, ExperimentalFactorDataclass
from src.model.vocabulary import Vocabulary
from tests.helpers import delete_fixture, post_fixture, put_fixture
from tests.router.study.fixture import AllStudyFixtureResponse


@dataclass
class ExperimentalFactorTypeResponse:
    maize_watering: Response
    barley_fungal_exposure: Response
    barley_zn_exposure: Response


@dataclass
class ExperimentalFactorResponse:
    factor_type_response: Response | None
    factor_response: Response
    study_response: list[Response]


@dataclass
class AllExperimentalFactorFixtureResponse:
    maize_watering: ExperimentalFactorResponse
    barley_fungal_exposure: ExperimentalFactorResponse
    barley_zn_exposure: ExperimentalFactorResponse
    study_response: AllStudyFixtureResponse


PATH = "experimentalFactor"
MAIZE_WATERING_TYPE = Vocabulary(title="Watering Type")
BARLEY_FUNGAL_EXPOSURE_TYPE = Vocabulary(
    title="arbuscular mycorrhizal fungal exposure", accession_number="PECO_0001059"
)
BARLEY_ZN_EXPOSURE_TYPE = Vocabulary(title="zinc nutrient exposure", accession_number="PECO:0007309")
MAIZE_WATERING_FACTOR = ExperimentalFactor(
    description="maize experiment factor",
    factor_description="Daily watering 1 L per plant.",
    factor_values="Watered; Unwatered",
)
BARLEY_FUNGAL_EXPOSURE_FACTOR = ExperimentalFactor(
    description="barley experiment factor",
    factor_description="Mycorrhizal-inoculation (Rhizophagus irregularis). The are two micorrhizal"
    "inoculation treatments (no micorrhizal inoculation (-) and micorrhizal inoculation(+))",
    factor_values="plus; minus",
)
BARLEY_ZN_EXPOSURE_FACTOR = ExperimentalFactor(
    description="barley experiment factor",
    factor_description="Soil Zn additions: 0, 10, 40, 90 mg/kg soil",
    factor_values="0, 10, 40, 90",
)


async def get_experimental_factor_fixture(
    data: ExperimentalFactor,
    studies: list[Response],
    test_client: AsyncTestClient,
    id: UUID | None = None,
    factor_type: Response | None = None,
) -> ExperimentalFactorResponse:
    study_id = [item.json()["id"] for item in studies]
    factor_type_id = factor_type.json()["id"] if factor_type else None
    send_data = ExperimentalFactorDataclass(study_id=study_id, factor_type_id=factor_type_id, **data.to_dict())
    if id is None:
        send_data.updated_at = None
        response = await post_fixture(PATH, send_data, test_client)
    else:
        response = await put_fixture(PATH, send_data, test_client, id)
    return ExperimentalFactorResponse(
        factor_response=response, factor_type_response=factor_type, study_response=studies
    )


@pytest.fixture(scope="function")
async def setup_factor_type(test_client: AsyncTestClient) -> AsyncGenerator[ExperimentalFactorTypeResponse, None]:
    maize_watering = await post_fixture("vocabulary", MAIZE_WATERING_TYPE, test_client)
    barley_fungal_exposure = await post_fixture("vocabulary", BARLEY_FUNGAL_EXPOSURE_TYPE, test_client)
    barley_zn_exposure = await post_fixture("vocabulary", BARLEY_ZN_EXPOSURE_TYPE, test_client)
    yield ExperimentalFactorTypeResponse(
        maize_watering=maize_watering,
        barley_fungal_exposure=barley_fungal_exposure,
        barley_zn_exposure=barley_zn_exposure,
    )
    await delete_fixture("vocabulary", maize_watering.json()["id"], test_client)
    await delete_fixture("vocabulary", barley_fungal_exposure.json()["id"], test_client)
    await delete_fixture("vocabulary", barley_zn_exposure.json()["id"], test_client)


@pytest.fixture(scope="function")
async def setup_experimental_factor(
    setup_study: AllStudyFixtureResponse,
    setup_factor_type: ExperimentalFactorTypeResponse,
    test_client: AsyncTestClient,
) -> AsyncGenerator[AllExperimentalFactorFixtureResponse, None]:
    maize_study = setup_study.maize.study_response
    barley_study = setup_study.barley.study_response
    maize_watering_type = setup_factor_type.maize_watering
    barley_zn_exposure_type = setup_factor_type.barley_zn_exposure
    barley_fungal_exposure_type = setup_factor_type.barley_fungal_exposure

    maize_watering_response = await get_experimental_factor_fixture(
        MAIZE_WATERING_FACTOR,
        [maize_study, barley_study],
        test_client,
        None,
        factor_type=maize_watering_type,
    )
    barley_fungal_exposure_response = await get_experimental_factor_fixture(
        BARLEY_FUNGAL_EXPOSURE_FACTOR,
        [barley_study],
        test_client,
        None,
        factor_type=barley_fungal_exposure_type,
    )
    barley_zn_exposure_response = await get_experimental_factor_fixture(
        BARLEY_ZN_EXPOSURE_FACTOR,
        [barley_study],
        test_client,
        None,
        factor_type=barley_zn_exposure_type,
    )
    yield AllExperimentalFactorFixtureResponse(
        maize_watering=maize_watering_response,
        barley_fungal_exposure=barley_fungal_exposure_response,
        barley_zn_exposure=barley_zn_exposure_response,
        study_response=setup_study,
    )
    await delete_fixture(PATH, maize_watering_response.factor_response.json()["id"], test_client)
    await delete_fixture(PATH, barley_fungal_exposure_response.factor_response.json()["id"], test_client)
    await delete_fixture(PATH, barley_zn_exposure_response.factor_response.json()["id"], test_client)


@pytest.fixture(scope="function")
async def update_experimental_factor(
    setup_experimental_factor: AllExperimentalFactorFixtureResponse, test_client: AsyncTestClient
) -> AsyncGenerator[AllExperimentalFactorFixtureResponse, None]:
    all_responses = setup_experimental_factor
    maize_study = all_responses.study_response.maize.study_response
    maize_watering_factor = all_responses.maize_watering
    response = await get_experimental_factor_fixture(
        MAIZE_WATERING_FACTOR,
        [maize_study],
        test_client,
        maize_watering_factor.factor_response.json()["id"],
    )
    all_responses.maize_watering = response
    yield all_responses
