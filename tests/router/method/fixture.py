from collections.abc import AsyncGenerator
from dataclasses import dataclass
from uuid import UUID

import pytest
from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.method import Method
from src.model.vocabulary import Vocabulary
from tests.helpers import delete_fixture, post_fixture, put_fixture


@dataclass
class MethodReferenceResponse:
    day_to_anthesis: Response
    projected_shoot_area: Response


@dataclass
class MethodResponse:
    method_reference_response: Response
    method_response: Response


@dataclass
class AllMethodFixtureResponse:
    day_to_anthesis: MethodResponse
    projected_shoot_area: MethodResponse
    method_reference: MethodReferenceResponse


PATH = "method"
DAY_TO_ANTHESIS_REF = Vocabulary(
    title="Days to Anthesis",
    accession_number="CO_322:0000189",
    external_reference="http://doi.org/10.2134/agronmonogr31.c2",
)
PROJECTED_SHOOT_AREA_REF = Vocabulary(
    title="Calculated Projected Shoot Area", external_reference="https://doi.org/10.1186/s13007-020-00577-6"
)
DAY_TO_ANTHESIS_METHOD = Method(
    name="Growing degree days to anthesis",
    description="Days to anthesis for male flowering "
    "was measured in thermal time (GDD: growing degree-days) "
    "according to Ritchie J, NeSmith D (1991;Temperature and crop development. "
    "Modeling plant and soil systems American Society of Agronomy Madison, Wisconsin USA) with TBASE=8°C and T0=30°C."
    "Plant height was measured at 5 years with a ruler, one year after Botritis inoculation.",
)
PROJECTED_SHOOT_AREA_METHOD = Method(
    name="calculated projected shoot area using camera images",
    description="Calculated as the sum of the number of plant pixels from 3 camera views (LemnaTec Scanalyzer 3D) "
    "comprising two side views and a view from above. The imaging data was prepared using the SET method "
    "check reference for the computations.",
)


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
