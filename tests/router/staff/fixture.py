from collections.abc import AsyncGenerator
from dataclasses import dataclass
from uuid import UUID

import pytest
from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.staff import Staff, StaffDataclass
from tests.helpers import delete_fixture, post_fixture, put_fixture
from tests.router.institution.fixture import AllInstitutionFixtureResponse


@dataclass
class StaffResponse:
    institution_response: list[Response]
    staff_response: Response


@dataclass
class AllStaffFixtureResponse:
    chris_b: StaffResponse
    step_w: StaffResponse
    john_doe: StaffResponse
    institution_response: AllInstitutionFixtureResponse


PATH = "staff"
CHRIS_B = Staff(name="Chris B", email="c.b@adelaide.edu.au", role="senior biometrician")
STEP_W = Staff(name="Steph W", email="s.w@adelaide.edu.au", role="project leader")
JOHN_DOE = Staff(name="John Doe", email="john.doe@adelaide.edu.au", role="SWE")


async def get_staff_fixture(
    data: Staff, institutions: list[Response], test_client: AsyncTestClient, id: UUID | None = None
) -> StaffResponse:
    institution_id = [item.json()["id"] for item in institutions]
    send_data = StaffDataclass(institution_id=institution_id, **data.to_dict())
    if id is None:
        send_data.updated_at = None
        response = await post_fixture(PATH, send_data, test_client)
    else:
        response = await put_fixture(PATH, send_data, test_client, id)
    return StaffResponse(institution_response=institutions, staff_response=response)


@pytest.fixture(scope="function")
async def setup_staff(
    setup_institutions: AllInstitutionFixtureResponse, test_client: AsyncTestClient
) -> AsyncGenerator[AllStaffFixtureResponse, None]:
    uoa_response = setup_institutions.UOA.institution_response
    appn_response = setup_institutions.APPN.institution_response
    tpa_response = setup_institutions.TPA.institution_response
    chris_b_response = await get_staff_fixture(CHRIS_B, [uoa_response, tpa_response], test_client)
    step_w_response = await get_staff_fixture(STEP_W, [uoa_response], test_client)
    john_doe_response = await get_staff_fixture(JOHN_DOE, [uoa_response, appn_response], test_client)
    yield AllStaffFixtureResponse(
        chris_b=chris_b_response,
        step_w=step_w_response,
        john_doe=john_doe_response,
        institution_response=setup_institutions,
    )
    await delete_fixture(PATH, chris_b_response.staff_response.json()["id"], test_client)
    await delete_fixture(PATH, john_doe_response.staff_response.json()["id"], test_client)
    await delete_fixture(PATH, step_w_response.staff_response.json()["id"], test_client)


@pytest.fixture(scope="function")
async def update_staff(
    setup_staff: AllStaffFixtureResponse, test_client: AsyncTestClient
) -> AsyncGenerator[AllStaffFixtureResponse, None]:
    all_responses = setup_staff
    uoa_response = setup_staff.institution_response.UOA.institution_response
    john_doe_response = await get_staff_fixture(
        JOHN_DOE, [uoa_response], test_client, setup_staff.john_doe.staff_response.json()["id"]
    )
    all_responses.john_doe = john_doe_response
    yield all_responses
