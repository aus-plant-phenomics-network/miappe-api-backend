import datetime
from collections.abc import AsyncGenerator

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


@pytest.fixture(scope="function")
async def setup_first_project(test_client: AsyncTestClient) -> AsyncGenerator[Response, None]:
    response = await post_fixture(PATH, FIRST_PROJECT, test_client)
    yield response
    await delete_fixture(PATH, response.json()["id"], test_client)


@pytest.fixture(scope="function")
async def update_first_project(
    setup_first_project: Response, test_client: AsyncTestClient
) -> AsyncGenerator[Response, None]:
    post_response = setup_first_project
    response = await put_fixture(PATH, FIRST_PROJECT_UPDATED, test_client, post_response.json()["id"])
    yield response


@pytest.fixture(scope="function")
async def setup_barley_project(test_client: AsyncTestClient) -> AsyncGenerator[Response, None]:
    response = await post_fixture(PATH, BARLEY_PROJECT_INVESTIGATION, test_client)
    yield response
    await delete_fixture(PATH, response.json()["id"], test_client)


@pytest.fixture(scope="function")
async def setup_maize_project(test_client: AsyncTestClient) -> AsyncGenerator[Response, None]:
    response = await post_fixture(PATH, MAIZE_PROJECT_INVESTIGATION, test_client)
    yield response
    await delete_fixture(PATH, response.json()["id"], test_client)
