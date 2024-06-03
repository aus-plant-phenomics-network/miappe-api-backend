import datetime
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from uuid import UUID

import pytest
from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.sample import Sample
from src.model.vocabulary import Vocabulary
from tests.helpers import delete_fixture, post_fixture, put_fixture
from tests.router.observation_unit.fixture import AllObservationUnitFixtureResponse

PATH = "sample"


@dataclass
class PlantStructuralDevelopmentResponse:
    PO_0007010: Response
    PO_0025094: Response


@dataclass
class PlantAnatomicalEntityResponse:
    PO_0025161: Response
    PO_0006001: Response


@dataclass
class SampleFixtureResponse:
    sample_response: Response
    plant_structural_development_response: Response
    plant_anatomical_entity_response: Response
    observation_unit_response: Response


@dataclass
class AllSampleFixtureResponse:
    leafdisc_061439: SampleFixtureResponse
    leafdisc_061440: SampleFixtureResponse
    cea_be00034067: SampleFixtureResponse
    structural_development_response: PlantStructuralDevelopmentResponse
    anatomical_entity_response: PlantAnatomicalEntityResponse
    observation_unit_response: AllObservationUnitFixtureResponse


PO_0025094 = Vocabulary(title="PO:0025094", accession_number="PO:0025094")
BBCH_17 = Vocabulary(title="BBCH-17", accession_number="BBCH-17")
PO_0007010 = Vocabulary(title="PO_0007010", accession_number="PO_0007010")
PO_0000003 = Vocabulary(title="PO:0000003", accession_number="PO:0000003")
PO_0025161 = Vocabulary(title="PO:0025161", accession_number="PO:0025161")
PO_0006001 = Vocabulary(title="PO_0006001", accession_number="PO_0006001")

LEAFDISC_061439 = Sample(
    title="leafdisc_061439",
    description="Leaves collected at harvest stage (Barley developmental stage 11)",
    collection_date=datetime.datetime(2017, 3, 8),
)

LEAFDISC_061440 = Sample(
    title="leafdisc_061440",
    description="Leaves collected at harvest stage (Barley developmental stage 11)",
    collection_date=datetime.datetime(2017, 3, 8),
)

CEA_BE00034067 = Sample(
    title="CEA:BE00034067",
    description="Distal part of the leaf ; 100 mg of roots taken from 10 roots at 20°C, conserved in vacuum at 20 mM NaCl salinity, stored at -60 °C to -85 °C.",
    collection_date=datetime.datetime(2005, 8, 15),
)


async def get_sample_fixture(
    data: Sample,
    structural_development: Response,
    anatomical_entity: Response,
    observation_unit: Response,
    test_client: AsyncTestClient,
    id: UUID | None = None,
) -> SampleFixtureResponse:
    structural_development_id = structural_development.json()["id"]
    anatomical_entity_id = anatomical_entity.json()["id"]
    observation_unit_id = observation_unit.json()["id"]
    send_data = Sample(
        plant_structural_development_stage_id=structural_development_id,
        plant_anatomical_entity_id=anatomical_entity_id,
        observation_unit_id=observation_unit_id,
        **data.to_dict(),
    )
    if id is None:
        send_data.updated_at = None
        response = await post_fixture(PATH, send_data, test_client)
    else:
        response = await put_fixture(PATH, send_data, test_client, id)
    return SampleFixtureResponse(
        plant_structural_development_response=structural_development,
        plant_anatomical_entity_response=anatomical_entity,
        observation_unit_response=observation_unit,
        sample_response=response,
    )


@pytest.fixture(scope="function")
async def setup_structural_development(
    test_client: AsyncTestClient,
) -> AsyncGenerator[PlantStructuralDevelopmentResponse, None]:
    PATH = "vocabulary"
    po_0007010 = await post_fixture(PATH, PO_0007010, test_client)
    po_0025094 = await post_fixture(PATH, PO_0025094, test_client)
    yield PlantStructuralDevelopmentResponse(PO_0007010=po_0007010, PO_0025094=po_0025094)
    await delete_fixture(PATH, po_0007010.json()["id"], test_client)
    await delete_fixture(PATH, po_0025094.json()["id"], test_client)


@pytest.fixture(scope="function")
async def setup_anatomical_entity(
    test_client: AsyncTestClient,
) -> AsyncGenerator[PlantAnatomicalEntityResponse, None]:
    PATH = "vocabulary"
    po_0006001 = await post_fixture(PATH, PO_0006001, test_client)
    po_0025161 = await post_fixture(PATH, PO_0025161, test_client)
    yield PlantAnatomicalEntityResponse(PO_0025161=po_0025161, PO_0006001=po_0006001)
    await delete_fixture(PATH, po_0006001.json()["id"], test_client)
    await delete_fixture(PATH, po_0025161.json()["id"], test_client)


@pytest.fixture(scope="function")
async def setup_sample(
    setup_structural_development: PlantStructuralDevelopmentResponse,
    setup_anatomical_entity: PlantAnatomicalEntityResponse,
    setup_observation_units: AllObservationUnitFixtureResponse,
    test_client: AsyncTestClient,
) -> AsyncGenerator[AllSampleFixtureResponse, None]:
    cea_be = await get_sample_fixture(
        CEA_BE00034067,
        setup_structural_development.PO_0025094,
        setup_anatomical_entity.PO_0025161,
        setup_observation_units.plot_894.observation_unit_response,
        test_client,
    )
    leafdisc_061439 = await get_sample_fixture(
        LEAFDISC_061439,
        setup_structural_development.PO_0007010,
        setup_anatomical_entity.PO_0006001,
        setup_observation_units.plant_061439.observation_unit_response,
        test_client,
    )
    leafdisc_061440 = await get_sample_fixture(
        LEAFDISC_061440,
        setup_structural_development.PO_0007010,
        setup_anatomical_entity.PO_0006001,
        setup_observation_units.plant_061440.observation_unit_response,
        test_client,
    )

    yield AllSampleFixtureResponse(
        leafdisc_061439=leafdisc_061439,
        leafdisc_061440=leafdisc_061440,
        cea_be00034067=cea_be,
        structural_development_response=setup_structural_development,
        anatomical_entity_response=setup_anatomical_entity,
        observation_unit_response=setup_observation_units,
    )
    await delete_fixture(PATH, cea_be.sample_response, test_client)
    await delete_fixture(PATH, leafdisc_061439.sample_response, test_client)
    await delete_fixture(PATH, leafdisc_061440.sample_response, test_client)
