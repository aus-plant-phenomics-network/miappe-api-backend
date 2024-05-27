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
