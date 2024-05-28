from collections.abc import AsyncGenerator
from dataclasses import dataclass
from uuid import UUID

import pytest
from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.data_file import DataFile, DataFileDataclass
from tests.helpers import delete_fixture, post_fixture, put_fixture
from tests.router.study.fixture import AllStudyFixtureResponse


@dataclass
class DataFileResponse:
    data_file_response: Response
    study_response: list[Response]


@dataclass
class AllDataFileFixtureResponse:
    maize: DataFileResponse
    barley: DataFileResponse
    study_response: AllStudyFixtureResponse


PATH = "dataFile"
BARLEY_DATA_FILE = DataFile(
    data_file_link="DOI : 10.25909/22875842.V1",
    data_file_description="Images and data from barley phenotyping studies performed at the APPF "
    "Plant Accelerator (TPA), University of Adelaide, on behalf of UA (Watts-Williams) ending 2017-04-20",
    data_file_version="1.0",
)

MAIZE_DATA_FILE = DataFile(
    data_file_link="http://www.ebi.ac.uk/arrayexpress/experiments/E-GEOD-32551/",
    data_file_description="FASTA tab-delimited column headers headers: 1. A 2. B 3. C",
    data_file_version="1.0",
)


async def get_data_file_fixture(
    data: DataFile, studies: list[Response], test_client: AsyncTestClient, id: UUID | None = None
) -> DataFileResponse:
    study_id = [item.json()["id"] for item in studies]
    send_data = DataFileDataclass(study_id=study_id, **data.to_dict())
    if id is None:
        send_data.updated_at = None
        response = await post_fixture(PATH, send_data, test_client)
    else:
        response = await put_fixture(PATH, send_data, test_client, id)
    return DataFileResponse(study_response=studies, data_file_response=response)


@pytest.fixture(scope="function")
async def setup_data_file(
    setup_study: AllStudyFixtureResponse, test_client: AsyncTestClient
) -> AsyncGenerator[AllDataFileFixtureResponse, None]:
    first_study = setup_study.first.study_response
    second_study = setup_study.second.study_response
    maize_study = setup_study.maize.study_response
    barley_response = await get_data_file_fixture(BARLEY_DATA_FILE, [first_study, second_study], test_client)
    maize_response = await get_data_file_fixture(MAIZE_DATA_FILE, [maize_study], test_client)

    yield AllDataFileFixtureResponse(maize=maize_response, barley=barley_response, study_response=setup_study)
    await delete_fixture(PATH, barley_response.data_file_response.json()["id"], test_client)
    await delete_fixture(PATH, maize_response.data_file_response.json()["id"], test_client)


@pytest.fixture(scope="function")
async def update_data_file(
    setup_data_file: AllDataFileFixtureResponse, test_client: AsyncTestClient
) -> AsyncGenerator[AllDataFileFixtureResponse, None]:
    all_responses = setup_data_file
    barley_study = all_responses.study_response.barley.study_response
    barley_data_file = all_responses.barley
    barley_response = await get_data_file_fixture(
        BARLEY_DATA_FILE, [barley_study], test_client, barley_data_file.data_file_response.json()["id"]
    )
    all_responses.barley = barley_response
    yield all_responses
