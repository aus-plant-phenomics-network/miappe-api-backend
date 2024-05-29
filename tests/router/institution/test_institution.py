from dataclasses import dataclass
from uuid import UUID

from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.institution import Institution, InstitutionDataclass
from tests.helpers import validate_post, validate_put
from tests.router.institution.fixture import (
    ANU,
    APPN,
    PATH,
    TPA,
    UOA,
    AllInstitutionFixtureResponse,
    InstitutionResponse,
)


@dataclass
class InstitutionFixture:
    id: UUID
    response: Response
    data: InstitutionDataclass


def get_institution_fixture(response: InstitutionResponse, data: Institution) -> InstitutionFixture:
    institution_response = response.institution_response
    institution_type_id = response.institution_type_response.json()["id"]
    parent_id = [item.json()["id"] for item in response.parent_response]
    fixture = InstitutionDataclass(institution_type_id=institution_type_id, parent_id=parent_id, **data.to_dict())
    return InstitutionFixture(id=institution_response.json()["id"], response=institution_response, data=fixture)


async def test_all_institutions_created(
    setup_institutions: AllInstitutionFixtureResponse, test_client: AsyncTestClient
) -> None:
    fixture = get_institution_fixture(setup_institutions.UOA, UOA)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_institution_fixture(setup_institutions.ANU, ANU)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_institution_fixture(setup_institutions.APPN, APPN)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_institution_fixture(setup_institutions.TPA, TPA)
    await validate_post(PATH, fixture.data, test_client, fixture.response)


async def test_tpa_updated(update_tpa_parents: AllInstitutionFixtureResponse, test_client: AsyncTestClient) -> None:
    fixture = get_institution_fixture(update_tpa_parents.TPA, TPA)
    await validate_put(PATH, fixture.data, test_client, fixture.response)


async def test_delete_anu(setup_institutions: AllInstitutionFixtureResponse, test_client: AsyncTestClient) -> None:
    anu_id = setup_institutions.ANU.institution_response.json()["id"]
    uoa_id = setup_institutions.UOA.institution_response.json()["id"]
    appn_id = setup_institutions.APPN.institution_response.json()["id"]
    await test_client.delete(f"{PATH}/{anu_id}")
    response = await test_client.get(f"{PATH}/{appn_id}")
    assert response.status_code == 200
    assert response.json()["parentId"] == [uoa_id]
