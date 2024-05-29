from collections.abc import AsyncGenerator
from dataclasses import dataclass
from uuid import UUID

import pytest
from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.facility import Facility
from src.model.vocabulary import Vocabulary
from tests.helpers import delete_fixture, post_fixture, put_fixture
from tests.router.institution.fixture import AllInstitutionFixtureResponse

PATH = "facility"


@dataclass
class FacilityResponse:
    facility_response: Response
    facility_type_response: Response
    institution_response: Response


@dataclass
class FacilityTypeResponse:
    greenhouse: Response
    field: Response


@dataclass
class AllFacilityFixtureResponse:
    inrae_field: FacilityResponse
    appn_greenhouse: FacilityResponse
    facility_type: FacilityTypeResponse
    institution: AllInstitutionFixtureResponse


GREENHOUSE_TYPE = Vocabulary(title="Greenhouse", accession_number="AGRO_00000363")

APPN_GREENHOUSE = Facility(
    name="TPA - Automated Greenhouse",
    description="Automated Greenhouse associated with the TPA/APPN",
    city="Adelaide",
    region="South Australia",
    country="Australia",
    postcode="5064",
    address="Waite Campus, Urrbrae SA",
    latitude="-34.971309538566246",
    longitude="+138.63947591867299",
    altitude="165m",
)

FIELD_CONDITION_TYPE = Vocabulary(title="Field environment condition", accession_number="CO_715:0000162")

INRAE_FIELD = Facility(
    name="INRAE - field environment condition",
    description="Field environment condition in the maize project",
    address="INRA, UE Diascope - Chemin de Mezouls - Domaine expérimental de Melgueil - 34130 Mauguio - France",
    country="France",
    postcode="34130",
    region="Mauguio",
    latitude="43.619264",
    longitude="3.967454",
    altitude="100m",
)


async def get_facility_fixture(
    data: Facility, institution: Response, facility_type: Response, test_client: AsyncTestClient, id: UUID | None = None
) -> FacilityResponse:
    institution_id = institution.json()["id"]
    facility_type_id = facility_type.json()["id"]
    send_data = Facility(institution_id=institution_id, facility_type_id=facility_type_id, **data.to_dict())
    if id is None:
        response = await post_fixture(PATH, send_data, test_client)
    else:
        response = await put_fixture(PATH, send_data, test_client, id)
    return FacilityResponse(
        institution_response=institution, facility_type_response=facility_type, facility_response=response
    )


@pytest.fixture(scope="function")
async def setup_facility_type(test_client: AsyncTestClient) -> AsyncGenerator[FacilityTypeResponse, None]:
    greenhouse = await post_fixture("vocabulary", GREENHOUSE_TYPE, test_client)
    field = await post_fixture("vocabulary", FIELD_CONDITION_TYPE, test_client)
    yield FacilityTypeResponse(greenhouse=greenhouse, field=field)
    await delete_fixture("vocabulary", greenhouse.json()["id"], test_client)
    await delete_fixture("vocabulary", field.json()["id"], test_client)


@pytest.fixture(scope="function")
async def setup_facility(
    setup_facility_type: FacilityTypeResponse,
    test_client: AsyncTestClient,
    setup_institutions: AllInstitutionFixtureResponse,
) -> AsyncGenerator[AllFacilityFixtureResponse, None]:
    appn = setup_institutions.APPN.institution_response
    greenhouse_type = setup_facility_type.greenhouse
    field_type = setup_facility_type.field
    appn_greenhouse = await get_facility_fixture(APPN_GREENHOUSE, appn, greenhouse_type, test_client)
    inrae_field = await get_facility_fixture(INRAE_FIELD, appn, field_type, test_client)

    yield AllFacilityFixtureResponse(
        appn_greenhouse=appn_greenhouse,
        inrae_field=inrae_field,
        facility_type=setup_facility_type,
        institution=setup_institutions,
    )
    await delete_fixture(PATH, appn_greenhouse.facility_response.json()["id"], test_client)
    await delete_fixture(PATH, inrae_field.facility_response.json()["id"], test_client)


@pytest.fixture(scope="function")
async def update_facility(
    setup_facility: AllFacilityFixtureResponse, test_client: AsyncTestClient
) -> AsyncGenerator[AllFacilityFixtureResponse, None]:
    all_response = setup_facility
    inrae = all_response.inrae_field
    field_type = all_response.facility_type.field
    inrae_institution = all_response.institution.INRAE.institution_response
    inrae_response = await get_facility_fixture(
        INRAE_FIELD, inrae_institution, field_type, test_client, inrae.facility_response.json()["id"]
    )
    all_response.inrae_field = inrae_response
    yield all_response
