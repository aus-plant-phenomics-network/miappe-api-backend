from uuid import UUID

from litestar.testing import AsyncTestClient

from tests.router.conftest import DATA_FILE_DESCRIPTION, DATA_FILE_LINK, DATA_FILE_TITLE, DATA_FILE_VERSION


async def test_create_data_files_successful(
    setup_data_file: tuple[UUID, UUID, UUID], test_client: AsyncTestClient
) -> None:
    data_file_id, first_id, second_id = setup_data_file
    response = await test_client.get(f"dataFile/{data_file_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == DATA_FILE_TITLE
    assert data["dataFileDescription"] == DATA_FILE_DESCRIPTION
    assert data["dataFileLink"] == DATA_FILE_LINK
    assert data["dataFileVersion"] == DATA_FILE_VERSION
    assert data["studyId"] == [first_id, second_id]


async def test_update_data_files_successful(
    update_data_file: tuple[UUID, UUID, UUID], test_client: AsyncTestClient
) -> None:
    data_file_id, first_id, second_id = update_data_file
    response = await test_client.get(f"dataFile/{data_file_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == DATA_FILE_TITLE
    assert data["dataFileDescription"] == DATA_FILE_DESCRIPTION
    assert data["dataFileLink"] == DATA_FILE_LINK
    assert data["dataFileVersion"] == DATA_FILE_VERSION
    assert data["studyId"] == [first_id]


async def test_delete_first_study_get_data_files(
    delete_first_study_get_data_file: tuple[UUID, UUID, UUID], test_client: AsyncTestClient
) -> None:
    data_file_id, first_id, second_id = delete_first_study_get_data_file
    response = await test_client.get(f"dataFile/{data_file_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == DATA_FILE_TITLE
    assert data["dataFileDescription"] == DATA_FILE_DESCRIPTION
    assert data["dataFileLink"] == DATA_FILE_LINK
    assert data["dataFileVersion"] == DATA_FILE_VERSION
    assert data["studyId"] == [second_id]
