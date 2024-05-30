from dataclasses import dataclass
from uuid import UUID

from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.experiment import Experiment, ExperimentDataclass
from tests.helpers import validate_post, validate_put
from tests.router.experiment.fixture import (
    BARLEY_EXPERIMENT,
    MAIZE_EXPERIMENT,
    PATH,
    AllExperimentFixtureResponse,
    ExperimentResponse,
)


@dataclass
class ExperimentFixture:
    id: UUID
    response: Response
    data: ExperimentDataclass
    study_id: UUID
    facility_id: list[UUID]
    staff_id: list[UUID]
    experiment_type_id: UUID


def get_experiment_fixture(response: ExperimentResponse, data: Experiment) -> ExperimentFixture:
    experiment_response = response.experiment_response
    study_id = response.study_response.json()["id"]
    facility_id = [item.json()["id"] for item in response.facility_response]
    staff_id = [item.json()["id"] for item in response.staff_response]
    experiment_type_id = response.experiment_type_response.json()["id"]
    fixture = ExperimentDataclass(
        study_id=study_id,
        facility_id=facility_id,
        staff_id=staff_id,
        experiment_type_id=experiment_type_id,
        **data.to_dict(),
    )
    return ExperimentFixture(
        id=experiment_response.json()["id"],
        response=experiment_response,
        data=fixture,
        study_id=study_id,
        facility_id=facility_id,
        staff_id=staff_id,
        experiment_type_id=experiment_type_id,
    )


async def test_all_experiments_created(
    setup_experiment: AllExperimentFixtureResponse, test_client: AsyncTestClient
) -> None:
    fixture = get_experiment_fixture(setup_experiment.maize, MAIZE_EXPERIMENT)
    await validate_post(PATH, fixture.data, test_client, fixture.response)

    fixture = get_experiment_fixture(setup_experiment.barley, BARLEY_EXPERIMENT)
    await validate_post(PATH, fixture.data, test_client, fixture.response)


async def test_barley_file_updated(
    update_experiment: AllExperimentFixtureResponse, test_client: AsyncTestClient
) -> None:
    fixture = get_experiment_fixture(update_experiment.maize, MAIZE_EXPERIMENT)
    await validate_put(PATH, fixture.data, test_client, fixture.response)
