from dataclasses import dataclass
from uuid import UUID

from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.biological_material import BiologicalMaterial, BiologicalMaterialDataclass
from tests.helpers import validate_post, validate_put
from tests.router.biological_material.fixture import (
    HORDEUM_MATERIAL,
    PATH,
    ZEA_MAYS_MATERIAL,
    AllBiologicalMaterialFixtureResponse,
    BiologicalMaterialResponse,
)


@dataclass
class BiologicalMaterialFixture:
    id: UUID
    response: Response
    data: BiologicalMaterialDataclass
    study_id: list[UUID]
    organism_id: UUID


def get_biological_material_fixture(
    response: BiologicalMaterialResponse, data: BiologicalMaterial
) -> BiologicalMaterialFixture:
    biological_material_response = response.biological_material_response
    study_id = [item.json()["id"] for item in response.study_response]
    organism_id = response.organism_response.json()["id"]
    fixture = BiologicalMaterialDataclass(
        study_id=study_id,
        organism_id=organism_id,
        **data.to_dict(),
    )
    return BiologicalMaterialFixture(
        id=biological_material_response.json()["id"],
        response=biological_material_response,
        data=fixture,
        study_id=study_id,
        organism_id=organism_id,
    )


async def test_all_biological_materials_created(
    setup_biological_material: AllBiologicalMaterialFixtureResponse, test_client: AsyncTestClient
) -> None:
    fixture = get_biological_material_fixture(setup_biological_material.zea_mays, ZEA_MAYS_MATERIAL)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_biological_material_fixture(setup_biological_material.hordeum, HORDEUM_MATERIAL)
    await validate_post(PATH, fixture.data, test_client, fixture.response)


async def test_biological_material_file_updated(
    update_biological_material: AllBiologicalMaterialFixtureResponse, test_client: AsyncTestClient
) -> None:
    fixture = get_biological_material_fixture(update_biological_material.zea_mays, ZEA_MAYS_MATERIAL)
    await validate_put(PATH, fixture.data, test_client, fixture.response)
