import datetime
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from uuid import UUID

import pytest
from httpx import Response
from litestar.testing import AsyncTestClient

from src.model import Study
from tests.helpers import delete_fixture, post_fixture, put_fixture
from tests.router.investigation.fixture import AllInvestigationFixtureResponse

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
    study_response: Response


@dataclass
class AllStudyFixtureResponse:
    first: StudyResponse
    second: StudyResponse
    barley: StudyResponse
    maize: StudyResponse
    investigation_response: AllInvestigationFixtureResponse


async def get_study_fixture(
    data: Study, investigation: Response, test_client: AsyncTestClient, id: UUID | None = None
) -> StudyResponse:
    investigation_id = investigation.json()["id"]
    send_data = Study(investigation_id=investigation_id, **data.to_dict())
    if id is None:
        response = await post_fixture(PATH, send_data, test_client)
    else:
        response = await put_fixture(PATH, send_data, test_client, id)
    return StudyResponse(study_response=response, investigation_response=investigation)


@pytest.fixture(scope="function")
async def setup_study(
    setup_investigation: AllInvestigationFixtureResponse, test_client: AsyncTestClient
) -> AsyncGenerator[AllStudyFixtureResponse, None]:
    first_response = await get_study_fixture(FIRST_STUDY, setup_investigation.first, test_client)
    second_response = await get_study_fixture(SECOND_STUDY, setup_investigation.first, test_client)
    barley_response = await get_study_fixture(BARLEY_PROJECT_STUDY, setup_investigation.barley, test_client)
    maize_response = await get_study_fixture(MAIZE_PROJECT_STUDY, setup_investigation.maize, test_client)
    yield AllStudyFixtureResponse(
        first=first_response,
        second=second_response,
        barley=barley_response,
        maize=maize_response,
        investigation_response=setup_investigation,
    )
    await delete_fixture(PATH, first_response.study_response.json()["id"], test_client)
    await delete_fixture(PATH, second_response.study_response.json()["id"], test_client)
    await delete_fixture(PATH, barley_response.study_response.json()["id"], test_client)
    await delete_fixture(PATH, maize_response.study_response.json()["id"], test_client)


@pytest.fixture(scope="function")
async def update_study(
    setup_study: AllStudyFixtureResponse, test_client: AsyncTestClient
) -> AsyncGenerator[AllStudyFixtureResponse, None]:
    all_response = setup_study
    first_id = all_response.first.study_response.json()["id"]
    first_response = await get_study_fixture(
        FIRST_STUDY_UPDATED, all_response.first.investigation_response, test_client, first_id
    )
    all_response.first = first_response
    yield all_response
