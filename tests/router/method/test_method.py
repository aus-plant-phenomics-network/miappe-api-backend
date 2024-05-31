from dataclasses import dataclass
from uuid import UUID

from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.method import Method
from tests.helpers import validate_post
from tests.router.method.fixture import (
    DAY_TO_ANTHESIS_METHOD,
    PATH,
    PROJECTED_SHOOT_AREA_METHOD,
    ZN_CONCENTRATION_METHOD,
    AllMethodFixtureResponse,
    MethodResponse,
)


@dataclass
class MethodFixture:
    id: UUID
    response: Response
    data: Method
    method_reference_id: UUID | None
    device_id: UUID | None = None


def get_method_fixture(response: MethodResponse, data: Method) -> MethodFixture:
    method_response = response.method_response
    method_reference_id = (
        response.method_reference_response.json()["id"] if response.method_reference_response else None
    )
    device_id = response.device_response.json()["id"] if response.device_response else None
    fixture = Method(method_reference_id=method_reference_id, **data.to_dict())
    return MethodFixture(
        id=method_response.json()["id"],
        response=method_response,
        data=fixture,
        method_reference_id=method_reference_id,
        device_id=device_id,
    )


async def test_methods_created(setup_method: AllMethodFixtureResponse, test_client: AsyncTestClient) -> None:
    fixture = get_method_fixture(setup_method.projected_shoot_area, PROJECTED_SHOOT_AREA_METHOD)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_method_fixture(setup_method.day_to_anthesis, DAY_TO_ANTHESIS_METHOD)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_method_fixture(setup_method.zn_concentration, ZN_CONCENTRATION_METHOD)
    await validate_post(PATH, fixture.data, test_client, fixture.response)
