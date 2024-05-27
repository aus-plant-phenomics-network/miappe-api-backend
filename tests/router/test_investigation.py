from uuid import UUID

from litestar.testing import AsyncTestClient

from tests.router.conftest import PROJECT_INIT_TITLE, PROJECT_UPDATED_DESCRIPTION, PROJECT_UPDATED_TITLE


async def test_investigation_created(setup_investigation: UUID, test_client: AsyncTestClient) -> None:
    item_id = setup_investigation
    response = await test_client.get(f"investigation/{item_id}")
    assert response.status_code == 200
    assert response.json()["title"] == PROJECT_INIT_TITLE


async def test_investigation_updated(setup_investigation: UUID, test_client: AsyncTestClient) -> None:
    item_id = setup_investigation
    response = await test_client.put(
        f"investigation/{item_id}", json={"title": PROJECT_UPDATED_TITLE, "description": PROJECT_UPDATED_DESCRIPTION}
    )
    assert response.status_code == 200
    assert response.json()["title"] == PROJECT_UPDATED_TITLE
    assert response.json()["description"] == PROJECT_UPDATED_DESCRIPTION


async def test_read_multiple_investigations(
    setup_investigation: UUID, setup_investigation_with_cleanup: UUID, test_client: AsyncTestClient
) -> None:
    first_id = setup_investigation
    second_id = setup_investigation_with_cleanup
    all_ids = {first_id, second_id}

    response = await test_client.get("investigation")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    db_ids = {item["id"] for item in data}
    assert all_ids == db_ids


async def test_delete_investigation(setup_investigation_no_cleanup: UUID, test_client: AsyncTestClient) -> None:
    item_id = setup_investigation_no_cleanup
    await test_client.delete(f"investigation/{item_id}")
    query_response = await test_client.get(f"investigation/{item_id}")
    assert query_response.status_code == 404


async def test_insert_projects_same_title_throws_error(setup_investigation: UUID, test_client: AsyncTestClient) -> None:
    _ = setup_investigation
    response = await test_client.post("investigation", json={"title": PROJECT_INIT_TITLE})
    assert response.status_code == 409
