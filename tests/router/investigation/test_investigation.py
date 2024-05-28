from dataclasses import dataclass
from uuid import UUID

from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.investigation import Investigation
from tests.helpers import delete_fixture, post_fixture, validate_get_not_exist, validate_post, validate_put
from tests.router.investigation.fixture import (
    BARLEY_PROJECT_INVESTIGATION,
    FIRST_PROJECT,
    FIRST_PROJECT_UPDATED,
    MAIZE_PROJECT_INVESTIGATION,
    PATH,
    AllInvestigationFixtureResponse,
)


@dataclass
class InvestigationFixture:
    id: UUID
    response: Response
    data: Investigation


def get_institution_fixture(response: Response, data: Investigation) -> InvestigationFixture:
    return InvestigationFixture(response=response, data=data, id=response.json()["id"])


async def test_first_project_created(
    setup_investigation: AllInvestigationFixtureResponse, test_client: AsyncTestClient
) -> None:
    fixture = get_institution_fixture(setup_investigation.first, FIRST_PROJECT)
    await validate_post(PATH, fixture.data, test_client, fixture.response)


async def test_first_project_updated(
    update_investigation: AllInvestigationFixtureResponse, test_client: AsyncTestClient
) -> None:
    fixture = get_institution_fixture(update_investigation.first, FIRST_PROJECT_UPDATED)
    await validate_put(PATH, fixture.data, test_client, fixture.response)


async def test_first_project_deleted(
    setup_investigation: AllInvestigationFixtureResponse, test_client: AsyncTestClient
) -> None:
    fixture = get_institution_fixture(setup_investigation.first, FIRST_PROJECT)
    response = await delete_fixture(PATH, fixture.id, test_client)
    assert response.status_code == 204
    await validate_get_not_exist(PATH, test_client, fixture.id)


async def test_create_project_same_name_throws_error(
    setup_investigation: AllInvestigationFixtureResponse, test_client: AsyncTestClient
) -> None:
    response = await post_fixture(PATH, FIRST_PROJECT, test_client)
    assert response.status_code == 409


async def test_barley_project_created(
    setup_investigation: AllInvestigationFixtureResponse, test_client: AsyncTestClient
) -> None:
    fixture = get_institution_fixture(setup_investigation.barley, BARLEY_PROJECT_INVESTIGATION)
    await validate_post(PATH, fixture.data, test_client, fixture.response)


async def test_maize_project_created(
    setup_investigation: AllInvestigationFixtureResponse, test_client: AsyncTestClient
) -> None:
    fixture = get_institution_fixture(setup_investigation.maize, MAIZE_PROJECT_INVESTIGATION)
    await validate_post(PATH, fixture.data, test_client, fixture.response)
