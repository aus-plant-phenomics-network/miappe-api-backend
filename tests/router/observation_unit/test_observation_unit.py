from dataclasses import dataclass
from uuid import UUID

from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.observation_unit import ObservationUnit, ObservationUnitDataclass
from tests.helpers import validate_post, validate_put
from tests.router.observation_unit.fixture import (
    PATH,
    PLANT_061439,
    PLANT_061440,
    PLOT_894,
    AllObservationUnitFixtureResponse,
    ObservationUnitResponse,
)


@dataclass
class ObservationUnitFixture:
    id: UUID
    response: Response
    data: ObservationUnitDataclass
    parent_id: list[UUID]
    experimental_factor_id: list[UUID]
    study_id: list[UUID]
    facility_id: UUID | None
    biological_material_id: UUID | None
    observation_unit_type_id: UUID | None


def get_observation_unit_fixture(response: ObservationUnitResponse, data: ObservationUnit) -> ObservationUnitFixture:
    observation_unit_response = response.observation_unit_response
    observation_unit_type_id = response.observation_unit_type_response.json()["id"]
    parent_id = [item.json()["id"] for item in response.parent_response]
    experimental_factor_id = [item.json()["id"] for item in response.experimental_factor_response]
    study_id = [item.json()["id"] for item in response.study_response]
    facility_id = response.facility_response.json()["id"] if response.facility_response else None
    biological_material_id = (
        response.biological_material_response.json()["id"] if response.biological_material_response else None
    )
    observation_unit_type_id = (
        response.observation_unit_type_response.json()["id"] if response.observation_unit_type_response else None
    )
    fixture = ObservationUnitDataclass(
        experimental_factor_id=experimental_factor_id,
        study_id=study_id,
        facility_id=facility_id,
        biological_material_id=biological_material_id,
        observation_unit_type_id=observation_unit_type_id,
        parent_id=parent_id,
        **data.to_dict(),
    )
    return ObservationUnitFixture(
        id=observation_unit_response.json()["id"],
        response=observation_unit_response,
        data=fixture,
        experimental_factor_id=experimental_factor_id,
        study_id=study_id,
        facility_id=facility_id,
        biological_material_id=biological_material_id,
        observation_unit_type_id=observation_unit_type_id,
        parent_id=parent_id,
    )


async def test_all_observation_units_created(
    setup_observation_units: AllObservationUnitFixtureResponse, test_client: AsyncTestClient
) -> None:
    fixture = get_observation_unit_fixture(setup_observation_units.plot_894, PLOT_894)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_observation_unit_fixture(setup_observation_units.plant_061439, PLANT_061439)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_observation_unit_fixture(setup_observation_units.plant_061440, PLANT_061440)
    await validate_post(PATH, fixture.data, test_client, fixture.response)


async def test_observation_unit_updated(
    update_observation_unit: AllObservationUnitFixtureResponse, test_client: AsyncTestClient
) -> None:
    fixture = get_observation_unit_fixture(update_observation_unit.plot_894, PLOT_894)
    await validate_put(PATH, fixture.data, test_client, fixture.response)
