from dataclasses import dataclass
from uuid import UUID

from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.sample import Sample
from tests.helpers import validate_post
from tests.router.sample.fixture import (
    CEA_BE00034067,
    LEAFDISC_061439,
    LEAFDISC_061440,
    PATH,
    AllSampleFixtureResponse,
    SampleFixtureResponse,
)


@dataclass
class SampleFixture:
    id: UUID
    response: Response
    data: Sample
    plant_structural_development_stage_id: UUID
    plant_anatomical_entity_id: UUID
    observation_unit_id: UUID


def get_sample_fixture(response: SampleFixtureResponse, data: Sample) -> SampleFixture:
    sample_response = response.sample_response
    plant_structural_development_stage_id = response.plant_structural_development_response.json()["id"]
    plant_anatomical_entity_id = response.plant_anatomical_entity_response.json()["id"]
    observation_unit_id = response.observation_unit_response.json()["id"]
    fixture = Sample(
        plant_structural_development_stage_id=plant_structural_development_stage_id,
        plant_anatomical_entity_id=plant_anatomical_entity_id,
        observation_unit_id=observation_unit_id,
        **data.to_dict(),
    )
    return SampleFixture(
        id=sample_response.json()["id"],
        response=sample_response,
        data=fixture,
        plant_structural_development_stage_id=plant_structural_development_stage_id,
        plant_anatomical_entity_id=plant_anatomical_entity_id,
        observation_unit_id=observation_unit_id,
    )


async def test_scanalyzer_created(setup_sample: AllSampleFixtureResponse, test_client: AsyncTestClient) -> None:
    fixture = get_sample_fixture(setup_sample.cea_be00034067, CEA_BE00034067)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_sample_fixture(setup_sample.leafdisc_061439, LEAFDISC_061439)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_sample_fixture(setup_sample.leafdisc_061440, LEAFDISC_061440)
    await validate_post(PATH, fixture.data, test_client, fixture.response)
