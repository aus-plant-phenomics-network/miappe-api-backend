from collections.abc import AsyncGenerator
from dataclasses import dataclass
from uuid import UUID

import pytest
from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.unit import Unit
from src.model.vocabulary import Vocabulary
from tests.helpers import delete_fixture, post_fixture, put_fixture


@dataclass
class UnitReferenceResponse:
    degree_day: Response


@dataclass
class UnitResponse:
    unit_reference_response: Response | None
    unit_response: Response


@dataclass
class AllUnitFixtureResponse:
    degree_day: UnitResponse
    kilo_pixel: UnitResponse
    microgram: UnitResponse


PATH = "unit"
DEGREE_DAY_REF = Vocabulary(
    title="Degree Day",
    accession_number="CO_322:0000510",
)
DEGREE_DAY_UNIT = Unit(name="Degree Day", symbol="°C day")
KILO_PIXEL_UNIT = Unit(name="Kilo Pixels", symbol="kp")
MICROGRAM_UNIT = Unit(name="Microgram", symbol="µg")


async def get_unit_fixture(
    data: Unit,
    test_client: AsyncTestClient,
    id: UUID | None = None,
    reference: Response | None = None,
) -> UnitResponse:
    unit_reference_id = reference.json()["id"] if reference else None
    send_data = Unit(unit_reference_id=unit_reference_id, **data.to_dict())
    if id is None:
        response = await post_fixture(PATH, send_data, test_client)
    else:
        response = await put_fixture(PATH, send_data, test_client, id)
    return UnitResponse(unit_reference_response=reference, unit_response=response)


@pytest.fixture(scope="function")
async def setup_unit_reference(test_client: AsyncTestClient) -> AsyncGenerator[UnitReferenceResponse, None]:
    degree_day = await post_fixture("vocabulary", DEGREE_DAY_REF, test_client)
    yield UnitReferenceResponse(degree_day=degree_day)
    await delete_fixture("vocabulary", degree_day.json()["id"], test_client)


@pytest.fixture(scope="function")
async def setup_unit(
    setup_unit_reference: UnitReferenceResponse, test_client: AsyncTestClient
) -> AsyncGenerator[AllUnitFixtureResponse, None]:
    unit = setup_unit_reference
    degree_day = await get_unit_fixture(DEGREE_DAY_UNIT, test_client, None, unit.degree_day)
    microgram = await get_unit_fixture(MICROGRAM_UNIT, test_client)
    kilo_pixel = await get_unit_fixture(KILO_PIXEL_UNIT, test_client)
    yield AllUnitFixtureResponse(degree_day=degree_day, microgram=microgram, kilo_pixel=kilo_pixel)
    await delete_fixture(PATH, degree_day.unit_response.json()["id"], test_client)
    await delete_fixture(PATH, microgram.unit_response.json()["id"], test_client)
    await delete_fixture(PATH, kilo_pixel.unit_response.json()["id"], test_client)
