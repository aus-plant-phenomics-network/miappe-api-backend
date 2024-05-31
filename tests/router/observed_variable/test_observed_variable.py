from dataclasses import dataclass
from uuid import UUID

from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.observed_variable import ObservedVariable, ObservedVariableDataclass
from tests.helpers import validate_post, validate_put
from tests.router.observed_variable.fixture import (
    ANTHESIS_VARIABLE,
    PATH,
    PROJECTED_SHOOT_AREA_VARIABLE,
    REPRODUCTIVE_GROWTH_TIME_VARIABLE,
    ZN_CONCENTRATION_VARIABLE,
    AllObservedVariableFixtureResponse,
    ObservedVariableResponse,
)


@dataclass
class ObservedVariableFixture:
    id: UUID
    response: Response
    data: ObservedVariableDataclass
    study_id: list[UUID]
    unit_id: UUID | None
    method_id: UUID | None
    trait_id: UUID | None


def get_observed_variable_fixture(
    response: ObservedVariableResponse, data: ObservedVariable
) -> ObservedVariableFixture:
    observed_variable_response = response.observed_variable_response
    study_id = [item.json()["id"] for item in response.study_response]
    unit_id = response.unit_response.json()["id"] if response.unit_response else None
    method_id = response.method_response.json()["id"] if response.method_response else None
    trait_id = response.trait_response.json()["id"] if response.trait_response else None
    fixture = ObservedVariableDataclass(
        study_id=study_id,
        method_id=method_id,
        unit_id=unit_id,
        trait_reference_id=trait_id,
        **data.to_dict(),
    )
    return ObservedVariableFixture(
        id=observed_variable_response.json()["id"],
        response=observed_variable_response,
        data=fixture,
        study_id=study_id,
        method_id=method_id,
        trait_id=trait_id,
        unit_id=unit_id,
    )


async def test_all_observed_variables_created(
    setup_observed_variable: AllObservedVariableFixtureResponse, test_client: AsyncTestClient
) -> None:
    fixture = get_observed_variable_fixture(setup_observed_variable.anthesis, ANTHESIS_VARIABLE)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_observed_variable_fixture(
        setup_observed_variable.reproductive_growth_time, REPRODUCTIVE_GROWTH_TIME_VARIABLE
    )
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_observed_variable_fixture(setup_observed_variable.projected_shoot_area, PROJECTED_SHOOT_AREA_VARIABLE)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_observed_variable_fixture(setup_observed_variable.zn_concentration, ZN_CONCENTRATION_VARIABLE)
    await validate_post(PATH, fixture.data, test_client, fixture.response)


async def test_observed_variable_file_updated(
    update_observed_variable: AllObservedVariableFixtureResponse, test_client: AsyncTestClient
) -> None:
    fixture = get_observed_variable_fixture(update_observed_variable.anthesis, ANTHESIS_VARIABLE)
    await validate_put(PATH, fixture.data, test_client, fixture.response)
