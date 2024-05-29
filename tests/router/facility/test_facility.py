from dataclasses import dataclass
from uuid import UUID

from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.facility import Facility
from tests.helpers import validate_post, validate_put
from tests.router.facility.fixture import (
    APPN_GREENHOUSE,
    INRAE_FIELD,
    PATH,
    AllFacilityFixtureResponse,
    FacilityResponse,
)


@dataclass
class FacilityFixture:
    id: UUID
    response: Response
    data: Facility
    facility_type_id: UUID
    institution_id: UUID


def get_facility_fixture(response: FacilityResponse, data: Facility) -> FacilityFixture:
    facility_response = response.facility_response
    facility_type_id = response.facility_type_response.json()["id"]
    institution_id = response.institution_response.json()["id"]

    fixture = Facility(facility_type_id=facility_type_id, institution_id=institution_id, **data.to_dict())
    return FacilityFixture(
        id=facility_response.json()["id"],
        response=facility_response,
        data=fixture,
        facility_type_id=facility_type_id,
        institution_id=institution_id,
    )


async def test_facility_created(setup_facility: AllFacilityFixtureResponse, test_client: AsyncTestClient) -> None:
    fixture = get_facility_fixture(setup_facility.appn_greenhouse, APPN_GREENHOUSE)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_facility_fixture(setup_facility.inrae_field, INRAE_FIELD)
    await validate_post(PATH, fixture.data, test_client, fixture.response)


async def test_update_facility(update_facility: AllFacilityFixtureResponse, test_client: AsyncTestClient) -> None:
    fixture = get_facility_fixture(update_facility.inrae_field, INRAE_FIELD)
    await validate_put(PATH, fixture.data, test_client, fixture.response)
