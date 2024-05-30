from dataclasses import dataclass
from uuid import UUID

from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.experimental_factor import ExperimentalFactor, ExperimentalFactorDataclass
from tests.helpers import validate_post, validate_put
from tests.router.experimental_factor.fixture import (
    BARLEY_FUNGAL_EXPOSURE_FACTOR,
    BARLEY_ZN_EXPOSURE_FACTOR,
    MAIZE_WATERING_FACTOR,
    PATH,
    AllExperimentalFactorFixtureResponse,
    ExperimentalFactorResponse,
)


@dataclass
class ExperimentalFactorFixture:
    id: UUID
    response: Response
    data: ExperimentalFactorDataclass
    study_id: list[UUID]
    factor_type_id: UUID | None


def get_experimental_factor_fixture(
    response: ExperimentalFactorResponse, data: ExperimentalFactor
) -> ExperimentalFactorFixture:
    factor_response = response.factor_response
    study_id = [item.json()["id"] for item in response.study_response]
    factor_type_id = response.factor_type_response.json()["id"] if response.factor_type_response else None
    fixture = ExperimentalFactorDataclass(study_id=study_id, factor_type_id=factor_type_id, **data.to_dict())
    return ExperimentalFactorFixture(
        id=factor_response.json()["id"],
        response=factor_response,
        data=fixture,
        study_id=study_id,
        factor_type_id=factor_type_id,
    )


async def test_all_experimental_factors_created(
    setup_experimental_factor: AllExperimentalFactorFixtureResponse, test_client: AsyncTestClient
) -> None:
    fixture = get_experimental_factor_fixture(setup_experimental_factor.maize_watering, MAIZE_WATERING_FACTOR)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_experimental_factor_fixture(setup_experimental_factor.barley_zn_exposure, BARLEY_ZN_EXPOSURE_FACTOR)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_experimental_factor_fixture(
        setup_experimental_factor.barley_fungal_exposure, BARLEY_FUNGAL_EXPOSURE_FACTOR
    )
    await validate_post(PATH, fixture.data, test_client, fixture.response)


async def test_experimental_factor_file_updated(
    update_experimental_factor: AllExperimentalFactorFixtureResponse, test_client: AsyncTestClient
) -> None:
    fixture = get_experimental_factor_fixture(update_experimental_factor.maize_watering, MAIZE_WATERING_FACTOR)
    await validate_put(PATH, fixture.data, test_client, fixture.response)