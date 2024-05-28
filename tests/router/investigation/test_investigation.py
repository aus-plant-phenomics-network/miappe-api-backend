from httpx import Response
from litestar.testing import AsyncTestClient

from tests.helpers import delete_fixture, post_fixture, validate_get_not_exist, validate_post, validate_put
from tests.router.investigation.conftest import (
    BARLEY_PROJECT_INVESTIGATION,
    FIRST_PROJECT,
    FIRST_PROJECT_UPDATED,
    MAIZE_PROJECT_INVESTIGATION,
    PATH,
)


async def test_first_project_created(setup_first_project: Response, test_client: AsyncTestClient) -> None:
    await validate_post(PATH, FIRST_PROJECT, test_client, setup_first_project)


async def test_first_project_updated(update_first_project: Response, test_client: AsyncTestClient) -> None:
    await validate_put(PATH, FIRST_PROJECT_UPDATED, test_client, update_first_project)


async def test_delete_first_project(setup_first_project: Response, test_client: AsyncTestClient) -> None:
    response = await delete_fixture(PATH, setup_first_project.json()["id"], test_client)
    assert response.status_code == 204
    await validate_get_not_exist(PATH, test_client, setup_first_project.json()["id"])


async def test_create_project_same_name_throws_error(
    setup_first_project: Response, test_client: AsyncTestClient
) -> None:
    response = await post_fixture(PATH, FIRST_PROJECT, test_client)
    assert response.status_code == 409


async def test_barley_project_created(setup_barley_project: Response, test_client: AsyncTestClient) -> None:
    await validate_post(PATH, BARLEY_PROJECT_INVESTIGATION, test_client, setup_barley_project)


async def test_maize_project_created(setup_maize_project: Response, test_client: AsyncTestClient) -> None:
    await validate_post(PATH, MAIZE_PROJECT_INVESTIGATION, test_client, setup_maize_project)
