import datetime
from collections.abc import AsyncGenerator
from dataclasses import dataclass

import pytest
from httpx import Response
from litestar.testing import AsyncTestClient

from src.model import Study
from tests.helpers import delete_fixture, post_fixture, put_fixture

PATH = "study"
FIRST_STUDY = Study(title="First Study", objective="First Study Objective", start_date=datetime.datetime(2022, 1, 1))
FIRST_STUDY_UPDATED = Study(
    title="First Study", objective="First Study Objective", start_date=datetime.datetime(2022, 1, 2)
)
SECOND_STUDY = Study(title="Second Study", objective="Second Study Objective", start_date=datetime.datetime(2022, 1, 1))
BARLEY_PROJECT_STUDY = Study(
    title="To test the response of barley to mycorrhizal inoculation when Zn is limiting, "
    "and also with increasing soil Zn concentration until Zn is almost phytotoxic.",
    objective="To test the response of barley to mycorrhizal inoculation when Zn is limiting, "
    "and also with increasing soil Zn concentration until Zn is almost phytotoxic."
    "High throughput phenotyping will be useful to track the growth responses to mycorrhizal colonisation over time, "
    "rather than just at the end (harvest) as is usually done. "
    "Use of the field spectrometer with leaf clip to measure tissue Zn over time will also be novel.",
    start_date=datetime.datetime(2017, 3, 1),
    end_date=datetime.datetime(2017, 4, 20),
)
MAIZE_PROJECT_STUDY = Study(
    title="2002 evaluation of flowering time for a panel of 375 maize lines at the experimental station of Maugio (France).",
    objective="2002 evaluation of male and female flowering time for a panel of 375 maize lines "
    "representing the worldwide genetic diversity at the experimental station of Maugio, France.",
    start_date=datetime.datetime(2002, 4, 4),
    end_date=datetime.datetime(2002, 11, 27),
)


@dataclass
class StudyResponse:
    investigation_response: Response
    study_response: Response | list[Response]


@pytest.fixture(scope="function")
async def setup_first_study(
    setup_first_project: Response, test_client: AsyncTestClient
) -> AsyncGenerator[StudyResponse, None]:
    investigation_response = setup_first_project
    first_study = Study(investigation_id=investigation_response.json()["id"], **FIRST_STUDY.to_dict())
    study_response = await post_fixture(PATH, first_study, test_client)
    yield StudyResponse(investigation_response=investigation_response, study_response=study_response)
    await delete_fixture(PATH, study_response.json()["id"], test_client)


@pytest.fixture(scope="function")
async def setup_first_and_second_study(
    setup_first_project: Response, test_client: AsyncTestClient
) -> AsyncGenerator[StudyResponse, None]:
    investigation_response = setup_first_project
    first_study = Study(investigation_id=investigation_response.json()["id"], **FIRST_STUDY.to_dict())
    second_study = Study(investigation_id=investigation_response.json()["id"], **SECOND_STUDY.to_dict())
    first_study_response = await post_fixture(PATH, first_study, test_client)
    second_study_response = await post_fixture(PATH, second_study, test_client)
    study_response = [first_study_response, second_study_response]
    yield StudyResponse(investigation_response=investigation_response, study_response=study_response)
    await delete_fixture(PATH, first_study_response.json()["id"], test_client)
    await delete_fixture(PATH, second_study_response.json()["id"], test_client)


@pytest.fixture(scope="function")
async def update_first_study(
    setup_first_study: StudyResponse, test_client: AsyncTestClient
) -> AsyncGenerator[StudyResponse, None]:
    study_response = setup_first_study.study_response
    investigation_response = setup_first_study.investigation_response
    if isinstance(study_response, list):
        study_response = study_response[0]
    updated_first_study = Study(investigation_id=investigation_response.json()["id"], **FIRST_STUDY_UPDATED.to_dict())
    response = await put_fixture(PATH, updated_first_study, test_client, study_response.json()["id"])
    yield StudyResponse(investigation_response=setup_first_study.investigation_response, study_response=response)


@pytest.fixture(scope="function")
async def setup_barley_study(
    setup_barley_project: Response, test_client: AsyncTestClient
) -> AsyncGenerator[StudyResponse, None]:
    project_id = setup_barley_project.json()["id"]
    barley_study = Study(investigation_id=project_id, **BARLEY_PROJECT_STUDY.to_dict())
    response = await post_fixture(PATH, barley_study, test_client)
    yield StudyResponse(investigation_response=setup_barley_project, study_response=response)
    await delete_fixture(PATH, response.json()["id"], test_client)


@pytest.fixture(scope="function")
async def setup_maize_study(
    setup_maize_project: Response, test_client: AsyncTestClient
) -> AsyncGenerator[StudyResponse, None]:
    project_id = setup_maize_project.json()["id"]
    maize_study = Study(investigation_id=project_id, **MAIZE_PROJECT_STUDY.to_dict())
    response = await post_fixture(PATH, maize_study, test_client)
    yield StudyResponse(investigation_response=setup_maize_project, study_response=response)
    await delete_fixture(PATH, response.json()["id"], test_client)
