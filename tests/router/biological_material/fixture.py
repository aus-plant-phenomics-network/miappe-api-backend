from collections.abc import AsyncGenerator
from dataclasses import dataclass
from uuid import UUID

import pytest
from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.biological_material import BiologicalMaterial, BiologicalMaterialDataclass
from src.model.vocabulary import Vocabulary
from tests.helpers import delete_fixture, post_fixture, put_fixture
from tests.router.study.fixture import AllStudyFixtureResponse


@dataclass
class OrganismResponse:
    zea_mays: Response
    hordeum: Response


@dataclass
class BiologicalMaterialResponse:
    biological_material_response: Response
    organism_response: Response
    study_response: list[Response]


@dataclass
class AllBiologicalMaterialFixtureResponse:
    zea_mays: BiologicalMaterialResponse
    hordeum: BiologicalMaterialResponse
    study_response: AllStudyFixtureResponse
    organism_response: OrganismResponse


PATH = "biologicalMaterial"
ZEA_MAYS_REFERENCE = Vocabulary(title="zea mays", accession_number="NCBITAXON:4577")
ZEA_MAYS_MATERIAL = BiologicalMaterial(
    title="INRA:W95115_inra_2001",
    genus="Zea Solanum",
    species="mays lycosperium x pennellii",
    infraspecific_name="vinifera Pinot noir B73 subspecies:vinifera ; "
    "cultivar:Pinot noir var:B73 subsp. vinifera var. Pinot Noir var. B73",
    biological_material_latitude="+39.067",
    biological_material_longitude="-8.73",
    biological_material_altitude="10 m",
    biological_material_coordinates_uncertainty="200 m",
    biological_material_preprocessing="EO:0007210 - PVY(NTN); transplanted from study "
    "http://phenome-fppn.fr/maugio/2013/t2351 observation unit ID: pot:894",
    material_source_id="INRA:W95115_inra ICNF:PNB-RPI",
    material_source_doi="doi:10.15454/1.4658436467893904E12",
    material_source_latitude="+39.067",
    material_source_longitude="-8.73",
    material_source_altitude="10 m",
    material_source_coordinates_uncertainty="200 m",
    material_source_description="Branches were collected from a 10-year-old tree growing in a progeny trial "
    "established in a loamy brown earth soil.",
)
HORDEUM_REFERENCE = Vocabulary(title="hordeum vulgare", accession_number="NCBITAXON:4513")
HORDEUM_MATERIAL = BiologicalMaterial(
    title="NCBITAXON:4513",
    genus="Hordeum",
    species="Hordeum vulgare",
    infraspecific_name="Compass",
)


async def get_biological_material_fixture(
    data: BiologicalMaterial,
    studies: list[Response],
    organism: Response,
    test_client: AsyncTestClient,
    id: UUID | None = None,
) -> BiologicalMaterialResponse:
    study_id = [item.json()["id"] for item in studies]
    organism_id = organism.json()["id"]
    send_data = BiologicalMaterialDataclass(study_id=study_id, organism_id=organism_id, **data.to_dict())
    if id is None:
        send_data.updated_at = None
        response = await post_fixture(PATH, send_data, test_client)
    else:
        response = await put_fixture(PATH, send_data, test_client, id)
    return BiologicalMaterialResponse(
        study_response=studies,
        biological_material_response=response,
        organism_response=organism,
    )


@pytest.fixture(scope="function")
async def setup_organism(test_client: AsyncTestClient) -> AsyncGenerator[OrganismResponse, None]:
    zea = await post_fixture("vocabulary", ZEA_MAYS_REFERENCE, test_client)
    hordeum = await post_fixture("vocabulary", HORDEUM_REFERENCE, test_client)
    yield OrganismResponse(zea_mays=zea, hordeum=hordeum)
    await delete_fixture("vocabulary", zea.json()["id"], test_client)
    await delete_fixture("vocabulary", hordeum.json()["id"], test_client)


@pytest.fixture(scope="function")
async def setup_biological_material(
    setup_study: AllStudyFixtureResponse,
    setup_organism: OrganismResponse,
    test_client: AsyncTestClient,
) -> AsyncGenerator[AllBiologicalMaterialFixtureResponse, None]:
    first_study = setup_study.first.study_response
    barley_study = setup_study.barley.study_response
    zea_organism = setup_organism.zea_mays
    hordeum_organism = setup_organism.hordeum
    zea_response = await get_biological_material_fixture(ZEA_MAYS_MATERIAL, [first_study], zea_organism, test_client)
    hordeum_response = await get_biological_material_fixture(
        HORDEUM_MATERIAL, [barley_study], hordeum_organism, test_client
    )
    yield AllBiologicalMaterialFixtureResponse(
        zea_mays=zea_response,
        hordeum=hordeum_response,
        study_response=setup_study,
        organism_response=setup_organism,
    )
    await delete_fixture(PATH, zea_response.biological_material_response.json()["id"], test_client)
    await delete_fixture(PATH, hordeum_response.biological_material_response.json()["id"], test_client)


@pytest.fixture(scope="function")
async def update_biological_material(
    setup_biological_material: AllBiologicalMaterialFixtureResponse, test_client: AsyncTestClient
) -> AsyncGenerator[AllBiologicalMaterialFixtureResponse, None]:
    all_responses = setup_biological_material
    maize_study = all_responses.study_response.maize.study_response
    zea = all_responses.zea_mays
    zea_organism = all_responses.organism_response.zea_mays
    zea_response = await get_biological_material_fixture(
        ZEA_MAYS_MATERIAL, [maize_study], zea_organism, test_client, zea.biological_material_response.json()["id"]
    )
    all_responses.zea_mays = zea_response
    yield all_responses
