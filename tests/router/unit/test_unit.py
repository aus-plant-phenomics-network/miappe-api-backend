from dataclasses import dataclass
from uuid import UUID

from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.unit import Unit
from tests.helpers import validate_post
from tests.router.unit.fixture import (
    DEGREE_DAY_UNIT,
    KILO_PIXEL_UNIT,
    MICROGRAM_UNIT,
    PATH,
    AllUnitFixtureResponse,
    UnitResponse,
)


@dataclass
class UnitFixture:
    id: UUID
    response: Response
    data: Unit
    unit_reference_id: UUID | None


def get_unit_fixture(response: UnitResponse, data: Unit) -> UnitFixture:
    unit_response = response.unit_response
    unit_reference_id = response.unit_reference_response.json()["id"] if response.unit_reference_response else None
    fixture = Unit(unit_reference_id=unit_reference_id, **data.to_dict())
    return UnitFixture(
        id=unit_response.json()["id"],
        response=unit_response,
        data=fixture,
        unit_reference_id=unit_reference_id,
    )


async def test_units_created(setup_unit: AllUnitFixtureResponse, test_client: AsyncTestClient) -> None:
    fixture = get_unit_fixture(setup_unit.kilo_pixel, KILO_PIXEL_UNIT)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_unit_fixture(setup_unit.microgram, MICROGRAM_UNIT)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_unit_fixture(setup_unit.degree_day, DEGREE_DAY_UNIT)
    await validate_post(PATH, fixture.data, test_client, fixture.response)
