from dataclasses import dataclass
from uuid import UUID

from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.data_file import DataFile, DataFileDataclass
from tests.helpers import validate_post, validate_put
from tests.router.data_file.fixture import (
    BARLEY_DATA_FILE,
    MAIZE_DATA_FILE,
    PATH,
    AllDataFileFixtureResponse,
    DataFileResponse,
)


@dataclass
class DataFileFixture:
    id: UUID
    response: Response
    data: DataFileDataclass
    study_id: list[UUID]


def get_data_file_fixture(response: DataFileResponse, data: DataFile) -> DataFileFixture:
    data_file_response = response.data_file_response
    study_id = [item.json()["id"] for item in response.study_response]
    fixture = DataFileDataclass(study_id=study_id, **data.to_dict())
    return DataFileFixture(
        id=data_file_response.json()["id"], response=data_file_response, data=fixture, study_id=study_id
    )


async def test_barley_file_created(setup_data_file: AllDataFileFixtureResponse, test_client: AsyncTestClient) -> None:
    fixture = get_data_file_fixture(setup_data_file.barley, BARLEY_DATA_FILE)
    await validate_post(PATH, fixture.data, test_client, fixture.response)


async def test_maize_file_created(setup_data_file: AllDataFileFixtureResponse, test_client: AsyncTestClient) -> None:
    fixture = get_data_file_fixture(setup_data_file.maize, MAIZE_DATA_FILE)
    await validate_post(PATH, fixture.data, test_client, fixture.response)


async def test_barley_file_updated(update_data_file: AllDataFileFixtureResponse, test_client: AsyncTestClient) -> None:
    fixture = get_data_file_fixture(update_data_file.barley, BARLEY_DATA_FILE)
    await validate_put(PATH, fixture.data, test_client, fixture.response)
