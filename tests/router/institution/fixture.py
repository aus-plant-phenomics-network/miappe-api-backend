from collections.abc import AsyncGenerator
from dataclasses import dataclass
from uuid import UUID

import pytest
from httpx import Response
from litestar.testing import AsyncTestClient

from src.model import Institution, Vocabulary
from src.model.institution import InstitutionDataclass
from tests.helpers import delete_fixture, post_fixture, put_fixture


@dataclass
class InstitutionTypeResponse:
    university: Response
    institute: Response


@dataclass
class InstitutionResponse:
    institution_response: Response
    parent_response: list[Response]
    institution_type_response: Response


@dataclass
class AllInstitutionFixtureResponse:
    UOA: InstitutionResponse
    ANU: InstitutionResponse
    APPN: InstitutionResponse
    TPA: InstitutionResponse
    institution_type: InstitutionTypeResponse


PATH = "institution"
TYPE_PATH = "vocabulary"
UNIVERSITY = Vocabulary(title="University", namespace="Research Institution Type")
RESEARCH_INSTITUTE = Vocabulary(title="Research Institute", namespace="Research Institution Type")
UOA = Institution(name="The University of Adelaide", country="Australia")
ANU = Institution(name="Australian National University", country="Australia")
APPN = Institution(name="Australian Plant Phenomics Network", country="Australia")
TPA = Institution(name="The Plant Accelerator", country="Australia")
UPARIS = Institution(name="University of Paris - XI", country="France")
UMR = Institution(name="UMR de Génétique Végétale", country="France")
INRAE = Institution(name="INRAE", country="France")


async def get_institution_fixture(
    institution_type: Response,
    data: Institution,
    parents: list[InstitutionResponse],
    test_client: AsyncTestClient,
    id: UUID | None = None,
) -> InstitutionResponse:
    institution_type_id = institution_type.json()["id"]
    parent_id = [item.institution_response.json()["id"] for item in parents]
    parsed_data = data.to_dict()
    post_data = InstitutionDataclass(institution_type_id=institution_type_id, parent_id=parent_id, **parsed_data)
    if id is None:
        post_data.updated_at = None
        response = await post_fixture(PATH, post_data, test_client)
    else:
        response = await put_fixture(PATH, post_data, test_client, id)
    return InstitutionResponse(
        institution_response=response,
        parent_response=[item.institution_response for item in parents],
        institution_type_response=institution_type,
    )


@pytest.fixture(scope="function")
async def setup_institution_type(test_client: AsyncTestClient) -> AsyncGenerator[InstitutionTypeResponse, None]:
    uni_response = await post_fixture(TYPE_PATH, UNIVERSITY, test_client)
    institute_response = await post_fixture(TYPE_PATH, RESEARCH_INSTITUTE, test_client)
    yield InstitutionTypeResponse(university=uni_response, institute=institute_response)
    await delete_fixture(TYPE_PATH, uni_response.json()["id"], test_client)
    await delete_fixture(TYPE_PATH, institute_response.json()["id"], test_client)


@pytest.fixture(scope="function")
async def setup_institutions(
    setup_institution_type: InstitutionTypeResponse, test_client: AsyncTestClient
) -> AsyncGenerator[AllInstitutionFixtureResponse, None]:
    uoa = await get_institution_fixture(setup_institution_type.university, UOA, [], test_client)
    anu = await get_institution_fixture(setup_institution_type.university, ANU, [], test_client)
    appn = await get_institution_fixture(setup_institution_type.institute, APPN, [uoa, anu], test_client)
    tpa = await get_institution_fixture(setup_institution_type.institute, TPA, [uoa, appn], test_client)
    yield AllInstitutionFixtureResponse(
        UOA=uoa,
        ANU=anu,
        APPN=appn,
        TPA=tpa,
        institution_type=setup_institution_type,
    )
    await delete_fixture(PATH, uoa.institution_response.json()["id"], test_client)
    await delete_fixture(PATH, anu.institution_response.json()["id"], test_client)
    await delete_fixture(PATH, appn.institution_response.json()["id"], test_client)
    await delete_fixture(PATH, tpa.institution_response.json()["id"], test_client)


@pytest.fixture(scope="function")
async def update_tpa_parents(
    setup_institutions: AllInstitutionFixtureResponse, test_client: AsyncTestClient
) -> AsyncGenerator[AllInstitutionFixtureResponse, None]:
    all_response = setup_institutions
    tpa = all_response.TPA
    tpa_response = await get_institution_fixture(
        all_response.institution_type.institute,
        TPA,
        [all_response.UOA],
        test_client,
        tpa.institution_response.json()["id"],
    )
    all_response.TPA = tpa_response
    yield all_response
