from uuid import UUID

from litestar.testing import AsyncTestClient

from tests.router.conftest import APPN_TITLE, COUNTRY, TPA_TITLE, UOA_TITLE


async def test_UOA_created(setup_UOA: tuple[UUID, UUID, UUID], test_client: AsyncTestClient) -> None:
    uoa_id, uni_id, department_id = setup_UOA
    response = await test_client.get(f"institution/{uoa_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == UOA_TITLE
    assert data["country"] == COUNTRY
    assert data["institutionTypeId"] == uni_id
    assert data["parentId"] == []


async def test_APPN_created(setup_APPN: tuple[UUID, UUID, UUID, UUID], test_client: AsyncTestClient) -> None:
    appn_id, uoa_id, uni_id, department_id = setup_APPN
    response = await test_client.get(f"institution/{appn_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == APPN_TITLE
    assert data["country"] == COUNTRY
    assert data["institutionTypeId"] == department_id
    assert data["parentId"] == [uoa_id]


async def test_TPA_created(setup_TPA: tuple[UUID, UUID, UUID, UUID, UUID], test_client: AsyncTestClient) -> None:
    tpa_id, appn_id, uoa_id, uni_id, department_id = setup_TPA
    response = await test_client.get(f"institution/{tpa_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == TPA_TITLE
    assert data["country"] == COUNTRY
    assert data["institutionTypeId"] == department_id
    assert data["parentId"] == [uoa_id]


async def test_TPA_updated(update_TPA: tuple[UUID, UUID, UUID, UUID, UUID], test_client: AsyncTestClient) -> None:
    tpa_id, appn_id, uoa_id, uni_id, department_id = update_TPA
    response = await test_client.get(f"institution/{tpa_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == TPA_TITLE
    assert data["country"] == COUNTRY
    assert data["institutionTypeId"] == department_id
    assert data["parentId"] == [uoa_id, appn_id]


async def test_delete_APPN(delete_APPN: tuple[UUID, UUID, UUID, UUID, UUID], test_client: AsyncTestClient) -> None:
    tpa_id, appn_id, uoa_id, uni_id, department_id = delete_APPN
    response = await test_client.get(f"institution/{tpa_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == TPA_TITLE
    assert data["country"] == COUNTRY
    assert data["institutionTypeId"] == department_id
    assert data["parentId"] == [uoa_id]
