import datetime
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from uuid import UUID

import pytest
from httpx import Response
from litestar.testing import AsyncTestClient

from src.model import Investigation
from tests.helpers import delete_fixture, post_fixture, put_fixture

PATH = "investigation"
FIRST_PROJECT = Investigation(title="First Project", description="First description")
FIRST_PROJECT_UPDATED = Investigation(title="First Project", description="First description updated")
BARLEY_PROJECT_INVESTIGATION = Investigation(
    title="To test the response of barley to mycorrhizal inoculation when Zn is limiting, "
    "and also with increasing soil Zn concentration until Zn is almost phytotoxic.",
    description="To test the response of barley to mycorrhizal inoculation when Zn is limiting, "
    "and also with increasing soil Zn concentration until Zn is almost phytotoxic."
    "High throughput phenotyping will be useful to track the growth responses to mycorrhizal colonisation over time, "
    "rather than just at the end (harvest) as is usually done. Use of the field spectrometer with leaf clip to measure "
    "tissue Zn over time will also be novel.",
    submission_date=datetime.datetime(2023, 5, 17),
    public_release_date=datetime.datetime(2023, 5, 17),
    license="CC BY-NC 4.0",
    publication_doi="10.34133/2019/5893953",
)
MAIZE_PROJECT_INVESTIGATION = Investigation(
    title="Adaptation of Maize to Temperate Climates: Mid-Density Genome-Wide Association Genetics and Diversity Patterns "
    "Reveal Key Genomic Regions, with a Major Contribution of the Vgt2 (ZCN8) Locus.",
    description="The migration of maize from tropical to temperate climates was accompanied by a dramatic evolution in flowering time. "
    "To gain insight into the genetic architecture of this adaptive trait, we conducted a 50K SNP-based genome-wide association "
    "and diversity investigation on a panel of tropical and temperate American and European representatives.",
    submission_date=datetime.datetime(2012, 12, 17),
    public_release_date=datetime.datetime(2013, 2, 25),
    license="CC BY-SA 4.0, Unreported",
    publication_doi="10.1371/journal.pone.0071377",
)


@dataclass
class AllInvestigationFixtureResponse:
    first: Response
    barley: Response
    maize: Response


async def get_investigation_fixture(
    data: Investigation, test_client: AsyncTestClient, id: UUID | None = None
) -> Response:
    send_data = Investigation(**data.to_dict())
    if id is None:
        response = await post_fixture(PATH, send_data, test_client)
    else:
        response = await put_fixture(PATH, send_data, test_client, id)
    return response


@pytest.fixture(scope="function")
async def setup_investigation(test_client: AsyncTestClient) -> AsyncGenerator[AllInvestigationFixtureResponse, None]:
    first_response = await get_investigation_fixture(FIRST_PROJECT, test_client)
    barley_response = await get_investigation_fixture(BARLEY_PROJECT_INVESTIGATION, test_client)
    maize_response = await get_investigation_fixture(MAIZE_PROJECT_INVESTIGATION, test_client)
    yield AllInvestigationFixtureResponse(first=first_response, barley=barley_response, maize=maize_response)
    await delete_fixture(PATH, first_response.json()["id"], test_client)
    await delete_fixture(PATH, barley_response.json()["id"], test_client)
    await delete_fixture(PATH, maize_response.json()["id"], test_client)


@pytest.fixture(scope="function")
async def update_investigation(
    setup_investigation: AllInvestigationFixtureResponse, test_client: AsyncTestClient
) -> AsyncGenerator[AllInvestigationFixtureResponse, None]:
    all_response = setup_investigation
    first_id = all_response.first.json()["id"]
    response = await get_investigation_fixture(FIRST_PROJECT_UPDATED, test_client, first_id)
    all_response.first = response
    yield all_response
