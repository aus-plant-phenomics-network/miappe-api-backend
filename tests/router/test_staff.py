from uuid import UUID

from litestar.testing import AsyncTestClient

from tests.router.conftest import STAFF_NAME, STAFF_ROLE


async def test_create_staff_successful(
    setup_staff: tuple[UUID, UUID, UUID, UUID], test_client: AsyncTestClient
) -> None:
    staff_id, tpa_id, appn_id, uoa_id = setup_staff
    response = await test_client.get(f"staff/{staff_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == STAFF_NAME
    assert data["role"] == STAFF_ROLE
    assert set(data["institutionId"]) == {tpa_id, appn_id}


async def test_update_staff_successful(
    update_staff: tuple[UUID, UUID, UUID, UUID], test_client: AsyncTestClient
) -> None:
    staff_id, tpa_id, appn_id, uoa_id = update_staff
    response = await test_client.get(f"staff/{staff_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == STAFF_NAME
    assert data["role"] == STAFF_ROLE
    assert set(data["institutionId"]) == {tpa_id, appn_id, uoa_id}


async def test_delete_TPA_get_staff(
    delete_tpa_get_staff: tuple[UUID, UUID, UUID, UUID], test_client: AsyncTestClient
) -> None:
    staff_id, tpa_id, appn_id, uoa_id = delete_tpa_get_staff
    response = await test_client.get(f"staff/{staff_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == STAFF_NAME
    assert data["role"] == STAFF_ROLE
    assert set(data["institutionId"]) == {appn_id}
