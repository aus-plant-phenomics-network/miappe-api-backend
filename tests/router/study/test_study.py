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
    StudyResponse,
)


@dataclass
class StudyFixture:
    response: Response
    data: Study
    investigation_id: UUID
    study_id: UUID


def get_study_fixture(
    response: StudyResponse,
    fixture_data: Study,
    study_index: int | None = None,
) -> StudyFixture:
    project = response.investigation_response
    project_id = project.json()["id"]
    data = Study(investigation_id=project_id, **fixture_data.to_dict())
    if study_index is None:
        assert not isinstance(response.study_response, list)
        study_response = response.study_response
    else:
        assert isinstance(response.study_response, list)
        assert len(response.study_response) > study_index
        study_response = response.study_response[study_index]
    return StudyFixture(
        response=study_response, data=data, investigation_id=project_id, study_id=study_response.json()["id"]
    )


async def test_first_study_created(setup_first_study: StudyResponse, test_client: AsyncTestClient) -> None:
    fixture = get_study_fixture(setup_first_study, FIRST_STUDY)
    await validate_post(PATH, fixture.data, test_client, fixture.response)


async def test_first_updated_created(update_first_study: StudyResponse, test_client: AsyncTestClient) -> None:
    fixture = get_study_fixture(update_first_study, FIRST_STUDY_UPDATED)
    await validate_put(PATH, fixture.data, test_client, fixture.response)


async def test_first_and_second_study_created(
    setup_first_and_second_study: StudyResponse, test_client: AsyncTestClient
) -> None:
    first = get_study_fixture(setup_first_and_second_study, FIRST_STUDY, 0)
    second = get_study_fixture(setup_first_and_second_study, SECOND_STUDY, 1)
    await validate_post(PATH, first.data, test_client, first.response)
    await validate_post(PATH, second.data, test_client, second.response)


async def test_delete_first_study(setup_first_study: StudyResponse, test_client: AsyncTestClient) -> None:
    fixture = get_study_fixture(setup_first_study, FIRST_STUDY)
    response = await test_client.delete(f"{PATH}/{fixture.study_id}")
    assert response.status_code == 204
    await validate_get_not_exist(PATH, test_client, fixture.study_id)


async def test_delete_first_project_also_delete_first_second_studies(
    setup_first_and_second_study: StudyResponse, test_client: AsyncTestClient
) -> None:
    first = get_study_fixture(setup_first_and_second_study, FIRST_STUDY, 0)
    second = get_study_fixture(setup_first_and_second_study, SECOND_STUDY, 1)
    response = await test_client.delete(f"investigation/{first.investigation_id}")
    assert response.status_code == 204
    await validate_get_not_exist(PATH, test_client, first.study_id)
    await validate_get_not_exist(PATH, test_client, second.study_id)


async def test_barley_study_created(setup_barley_study: StudyResponse, test_client: AsyncTestClient) -> None:
    fixture = get_study_fixture(setup_barley_study, BARLEY_PROJECT_STUDY)
    await validate_post(PATH, fixture.data, test_client, fixture.response)


async def test_maize_study_created(setup_maize_study: StudyResponse, test_client: AsyncTestClient) -> None:
    fixture = get_study_fixture(setup_maize_study, MAIZE_PROJECT_STUDY)
    await validate_post(PATH, fixture.data, test_client, fixture.response)
