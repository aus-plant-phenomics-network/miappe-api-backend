from dataclasses import dataclass
from uuid import UUID

from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.staff import Staff, StaffDataclass
from tests.helpers import validate_post, validate_put
from tests.router.staff.fixture import CHRIS_B, JOHN_DOE, PATH, STEP_W, AllStaffFixtureResponse, StaffResponse


@dataclass
class StaffFixture:
    id: UUID
    response: Response
    data: StaffDataclass


def get_staff_fixture(response: StaffResponse, data: Staff) -> StaffFixture:
    staff_response = response.staff_response
    institution_id = [item.json()["id"] for item in response.institution_response]
    fixture = StaffDataclass(institution_id=institution_id, **data.to_dict())
    return StaffFixture(id=staff_response.json()["id"], response=staff_response, data=fixture)


async def test_chris_b_created(setup_staff: AllStaffFixtureResponse, test_client: AsyncTestClient) -> None:
    fixture = get_staff_fixture(setup_staff.chris_b, CHRIS_B)
    await validate_post(PATH, fixture.data, test_client, fixture.response)


async def test_step_w_created(setup_staff: AllStaffFixtureResponse, test_client: AsyncTestClient) -> None:
    fixture = get_staff_fixture(setup_staff.step_w, STEP_W)
    await validate_post(PATH, fixture.data, test_client, fixture.response)


async def test_john_doe_created(setup_staff: AllStaffFixtureResponse, test_client: AsyncTestClient) -> None:
    fixture = get_staff_fixture(setup_staff.john_doe, JOHN_DOE)
    await validate_post(PATH, fixture.data, test_client, fixture.response)


async def test_john_doe_updated(update_staff: AllStaffFixtureResponse, test_client: AsyncTestClient) -> None:
    fixture = get_staff_fixture(update_staff.john_doe, JOHN_DOE)
    await validate_put(PATH, fixture.data, test_client, fixture.response)


async def test_delete_appn(setup_staff: AllStaffFixtureResponse, test_client: AsyncTestClient) -> None:
    appn_id = setup_staff.institution_response.APPN.institution_response.json()["id"]
    uoa_id = setup_staff.institution_response.UOA.institution_response.json()["id"]
    await test_client.delete(f"institution/{appn_id}")
    john_doe_id = setup_staff.john_doe.staff_response.json()["id"]
    response = await test_client.get(f"{PATH}/{john_doe_id}")
    assert response.status_code == 200
    assert response.json()["institutionId"] == [uoa_id]
