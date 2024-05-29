from dataclasses import dataclass
from uuid import UUID

from httpx import Response
from litestar.testing import AsyncTestClient

from src.model import Study
from tests.helpers import validate_get_not_exist, validate_post, validate_put
from tests.router.study.fixture import (
    BARLEY_PROJECT_STUDY,
    FIRST_STUDY,
    FIRST_STUDY_UPDATED,
    MAIZE_PROJECT_STUDY,
    PATH,
    SECOND_STUDY,
    AllStudyFixtureResponse,
    StudyResponse,
)


@dataclass
class StudyFixture:
    id: UUID
    response: Response
    data: Study
    investigation_id: UUID


def get_study_fixture(
    response: StudyResponse,
    data: Study,
) -> StudyFixture:
    study_response = response.study_response
    project = response.investigation_response
    project_id = project.json()["id"]
    data = Study(investigation_id=project_id, **data.to_dict())
    return StudyFixture(response=study_response, data=data, investigation_id=project_id, id=study_response.json()["id"])


async def test_all_studies_created(setup_study: AllStudyFixtureResponse, test_client: AsyncTestClient) -> None:
    fixture = get_study_fixture(setup_study.first, FIRST_STUDY)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_study_fixture(setup_study.barley, BARLEY_PROJECT_STUDY)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_study_fixture(setup_study.maize, MAIZE_PROJECT_STUDY)
    await validate_post(PATH, fixture.data, test_client, fixture.response)


async def test_first_updated_created(update_study: AllStudyFixtureResponse, test_client: AsyncTestClient) -> None:
    fixture = get_study_fixture(update_study.first, FIRST_STUDY_UPDATED)
    await validate_put(PATH, fixture.data, test_client, fixture.response)


async def test_delete_first_study(setup_study: AllStudyFixtureResponse, test_client: AsyncTestClient) -> None:
    fixture = get_study_fixture(setup_study.first, FIRST_STUDY)
    response = await test_client.delete(f"{PATH}/{fixture.id}")
    assert response.status_code == 204
    await validate_get_not_exist(PATH, test_client, fixture.id)


async def test_delete_first_project_also_delete_first_and_second_studies(
    setup_study: AllStudyFixtureResponse, test_client: AsyncTestClient
) -> None:
    first = get_study_fixture(setup_study.first, FIRST_STUDY)
    second = get_study_fixture(setup_study.second, SECOND_STUDY)
    response = await test_client.delete(f"investigation/{first.investigation_id}")
    assert response.status_code == 204
    await validate_get_not_exist(PATH, test_client, first.id)
    await validate_get_not_exist(PATH, test_client, second.id)
