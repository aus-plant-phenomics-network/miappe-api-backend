from uuid import UUID

from litestar.testing import AsyncTestClient

from tests.router.conftest import (
    STUDY_INIT_END_DATE,
    STUDY_INIT_OBJECTIVE,
    STUDY_INIT_START_DATE,
    STUDY_INIT_TITLE,
    STUDY_UPDATED_END_DATE,
    STUDY_UPDATED_OBJECTIVE,
    STUDY_UPDATED_START_DATE,
    STUDY_UPDATED_TITLE,
)


async def test_study_created(setup_study: tuple[UUID, UUID], test_client: AsyncTestClient) -> None:
    project_id, study_id = setup_study
    response = await test_client.get(f"study/{study_id}")
    assert response.status_code == 200
    assert response.json()["title"] == STUDY_INIT_TITLE
    assert response.json()["objective"] == STUDY_INIT_OBJECTIVE
    assert response.json()["startDate"] == STUDY_INIT_START_DATE
    assert response.json()["endDate"] == STUDY_INIT_END_DATE
    assert response.json()["investigationId"] == project_id


async def test_study_updated(update_study: tuple[UUID, UUID], test_client: AsyncTestClient) -> None:
    project_id, study_id = update_study
    response = await test_client.get(f"study/{study_id}")
    assert response.status_code == 200
    assert response.json()["title"] == STUDY_UPDATED_TITLE
    assert response.json()["objective"] == STUDY_UPDATED_OBJECTIVE
    assert response.json()["startDate"] == STUDY_UPDATED_START_DATE
    assert response.json()["endDate"] == STUDY_UPDATED_END_DATE
    assert response.json()["investigationId"] == project_id


async def test_deleting_project_also_removes_study(
    setup_study: tuple[UUID, UUID], test_client: AsyncTestClient
) -> None:
    project_id, study_id = setup_study
    await test_client.delete(f"investigation/{project_id}")
    response = await test_client.get(f"study/{study_id}")
    assert response.status_code == 404
