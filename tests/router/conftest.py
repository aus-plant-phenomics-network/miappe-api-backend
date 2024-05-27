from collections.abc import AsyncGenerator
from uuid import UUID

import pytest
from litestar.testing import AsyncTestClient

PROJECT_INIT_TITLE = "First Project"
PROJECT_UPDATED_TITLE = "First Investigation"
PROJECT_UPDATED_DESCRIPTION = "Project Description"


@pytest.fixture(scope="function")
async def setup_investigation(test_client: AsyncTestClient) -> AsyncGenerator[UUID, None]:
    response = await test_client.post("/investigation", json={"title": PROJECT_INIT_TITLE})
    assert response.status_code == 201
    response_id = response.json()["id"]
    yield response_id

    await test_client.delete(f"investigation/{response_id}")


@pytest.fixture(scope="function")
async def setup_investigation_no_cleanup(test_client: AsyncTestClient) -> AsyncGenerator[UUID, None]:
    response = await test_client.post(
        "/investigation", json={"title": PROJECT_UPDATED_TITLE, "description": PROJECT_UPDATED_DESCRIPTION}
    )
    assert response.status_code == 201
    response_id = response.json()["id"]
    yield response_id


@pytest.fixture(scope="function")
async def setup_investigation_with_cleanup(test_client: AsyncTestClient) -> AsyncGenerator[UUID, None]:
    response = await test_client.post(
        "/investigation", json={"title": PROJECT_UPDATED_TITLE, "description": PROJECT_UPDATED_DESCRIPTION}
    )
    assert response.status_code == 201
    response_id = response.json()["id"]
    yield response_id

    await test_client.delete(f"investigation/{response_id}")


# Study fixture
STUDY_INIT_TITLE = "First study"
STUDY_INIT_OBJECTIVE = "Study Objective"
STUDY_INIT_START_DATE = "2020-01-01T00:00:00"
STUDY_INIT_END_DATE = "2020-05-01T00:00:00"

STUDY_UPDATED_TITLE = "First study updated"
STUDY_UPDATED_OBJECTIVE = "Study Objective updated"
STUDY_UPDATED_START_DATE = "2020-01-05T00:00:00"
STUDY_UPDATED_END_DATE = "2020-05-05T00:00:00"


@pytest.fixture(scope="function")
async def setup_study(
    setup_investigation: UUID, test_client: AsyncTestClient
) -> AsyncGenerator[tuple[UUID, UUID], None]:
    project_id = setup_investigation
    response = await test_client.post(
        "study",
        json={
            "title": STUDY_INIT_TITLE,
            "objective": STUDY_INIT_OBJECTIVE,
            "startDate": STUDY_INIT_START_DATE,
            "endDate": STUDY_INIT_END_DATE,
            "investigationId": project_id,
        },
    )
    assert response.status_code == 201
    study_id = response.json()["id"]
    yield (project_id, study_id)
    await test_client.delete(f"study/{study_id}")


@pytest.fixture(scope="function")
async def setup_second_study(
    setup_investigation: UUID, test_client: AsyncTestClient
) -> AsyncGenerator[tuple[UUID, UUID], None]:
    project_id = setup_investigation
    response = await test_client.post(
        "study",
        json={
            "title": STUDY_UPDATED_TITLE,
            "objective": STUDY_UPDATED_OBJECTIVE,
            "startDate": STUDY_UPDATED_START_DATE,
            "endDate": STUDY_UPDATED_END_DATE,
            "investigationId": project_id,
        },
    )
    assert response.status_code == 201
    study_id = response.json()["id"]
    yield (project_id, study_id)
    await test_client.delete(f"study/{study_id}")


@pytest.fixture(scope="function")
async def update_study(
    setup_study: tuple[UUID, UUID], setup_investigation_with_cleanup: UUID, test_client: AsyncTestClient
) -> AsyncGenerator[tuple[UUID, UUID], None]:
    project_id = setup_investigation_with_cleanup
    _, study_id = setup_study
    response = await test_client.put(
        f"study/{study_id}",
        json={
            "title": STUDY_UPDATED_TITLE,
            "objective": STUDY_UPDATED_OBJECTIVE,
            "startDate": STUDY_UPDATED_START_DATE,
            "endDate": STUDY_UPDATED_END_DATE,
            "investigationId": project_id,
        },
    )
    assert response.status_code == 200
    yield (project_id, study_id)
