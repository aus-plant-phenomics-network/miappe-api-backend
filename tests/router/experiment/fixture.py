import datetime
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from uuid import UUID

import pytest
from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.experiment import Experiment, ExperimentDataclass
from src.model.vocabulary import Vocabulary
from tests.helpers import delete_fixture, post_fixture, put_fixture
from tests.router.facility.fixture import AllFacilityFixtureResponse
from tests.router.staff.fixture import AllStaffFixtureResponse
from tests.router.study.fixture import AllStudyFixtureResponse


@dataclass
class ExperimentTypeResponse:
    maize: Response
    barley: Response


@dataclass
class ExperimentResponse:
    experiment_response: Response
    study_response: Response
    experiment_type_response: Response
    facility_response: list[Response]
    staff_response: list[Response]


@dataclass
class AllExperimentFixtureResponse:
    maize: ExperimentResponse
    barley: ExperimentResponse
    study_response: AllStudyFixtureResponse
    experiment_type_response: ExperimentTypeResponse
    facility_response: AllFacilityFixtureResponse
    staff_response: AllStaffFixtureResponse


PATH = "experiment"

MAIZE_EXPERIMENT_TYPE = Vocabulary(title="maize experiment design", accession_number="CO_715:0000145")
BARLEY_EXPERIMENT_TYPE = Vocabulary(title="barley experiment design", accession_number="OBI_0500007")
MAIZE_EXPERIMENT = Experiment(
    title="2002 evaluation of flowering time for a panel of 375 maize lines at the experimental station of Maugio (France).",
    objective="2002 evaluation of male and female flowering time for a panel of 375 maize lines "
    "representing the worldwide genetic diversity at the experimental station of Maugio, France.",
    start_date=datetime.datetime(2002, 4, 4),
    end_date=datetime.datetime(2002, 11, 27),
    observation_unit_level_hierarchy="block>rep>plot",
    observation_unit_level_description="Observation units consisted in individual plots "
    "themselves consisting of a row of 15 plants at a density of approximately six plants per square meter.",
    cultural_practices="Irrigation was applied according needs during summer to prevent water stress.",
    map_of_experimental_design="https://urgi.versailles.inra.fr/files/ephesis/181000503/181000503_plan.xls",
    description_of_experimental_design="Lines were repeated twice at each location using a complete block design. "
    "In order to limit competition effects, each block was organized into four sub-blocks corresponding to earliness"
    "groups based on a priori information. ",
)
BARLEY_EXPERIMENT = Experiment(
    title="To test the response of barley to mycorrhizal inoculation when Zn is limiting, "
    "and also with increasing soil Zn concentration until Zn is almost phytotoxic.",
    objective="To test the response of barley to mycorrhizal inoculation when Zn is limiting, "
    "and also with increasing soil Zn concentration until Zn is almost phytotoxic."
    "High throughput phenotyping will be useful to track the growth responses"
    "to mycorrhizal colonisation over time, rather than just at the end (harvest)"
    "as is usually done. Use of the field spectrometer with leaf clip to measure tissue Zn over time will also be novel.",
    start_date=datetime.datetime(2017, 3, 1),
    end_date=datetime.datetime(2017, 4, 20),
    observation_unit_level_hierarchy="block>rep>pot",
    observation_unit_level_description="Observation units consisted of individual plants in pots with 4 replicates of the 8 treatments.",
    cultural_practices="150 mm pots, Soil Custom: 1:9 autoclaved Arboretum soil/autoclaved play sand, with or without"
    "mycorrhizal inoculum, Fertilizer: 1/2 strength Long-Ashton Zn P (given once per week at rate of approx. 20mL) "
    "once weekly, Watering frequence: daily, Water amount / pot: Water to designated"
    "weight (TBD)",
    map_of_experimental_design="File name: Exp380_381DesignSummary.pdf",
    description_of_experimental_design="The design for each experiment is a"
    "randomized complete block design with 4 replicates of the 8 treatments. Two replicates are located in each of"
    "two lanes in the South West Smarthouse. The design was randomized using dae (Brien, 2016), a package for the R"
    "statistical computing environment (R Development Core Team, 2016). ",
)


async def get_experiment_fixture(
    data: Experiment,
    study: Response,
    experiment_type: Response,
    staffs: list[Response],
    facilities: list[Response],
    test_client: AsyncTestClient,
    id: UUID | None = None,
) -> ExperimentResponse:
    facility_id = [item.json()["id"] for item in facilities]
    staff_id = [item.json()["id"] for item in staffs]
    study_id = study.json()["id"]
    experiment_type_id = experiment_type.json()["id"]
    send_data = ExperimentDataclass(
        study_id=study_id,
        facility_id=facility_id,
        experiment_type_id=experiment_type_id,
        staff_id=staff_id,
        **data.to_dict(),
    )
    if id is None:
        send_data.updated_at = None
        response = await post_fixture(PATH, send_data, test_client)
    else:
        response = await put_fixture(PATH, send_data, test_client, id)
    return ExperimentResponse(
        study_response=study,
        experiment_response=response,
        experiment_type_response=experiment_type,
        facility_response=facilities,
        staff_response=staffs,
    )


@pytest.fixture(scope="function")
async def setup_experiment_type(test_client: AsyncTestClient) -> AsyncGenerator[ExperimentTypeResponse, None]:
    maize = await post_fixture("vocabulary", MAIZE_EXPERIMENT_TYPE, test_client)
    barley = await post_fixture("vocabulary", BARLEY_EXPERIMENT_TYPE, test_client)
    yield ExperimentTypeResponse(maize=maize, barley=barley)
    await delete_fixture("vocabulary", maize.json()["id"], test_client)
    await delete_fixture("vocabulary", barley.json()["id"], test_client)


@pytest.fixture(scope="function")
async def setup_experiment(
    setup_experiment_type: ExperimentTypeResponse,
    setup_study: AllStudyFixtureResponse,
    setup_staff: AllStaffFixtureResponse,
    setup_facility: AllFacilityFixtureResponse,
    test_client: AsyncTestClient,
) -> AsyncGenerator[AllExperimentFixtureResponse, None]:
    first_study = setup_study.first.study_response
    maize_type = setup_experiment_type.maize
    barley_type = setup_experiment_type.barley
    step_w = setup_staff.step_w
    chris_b = setup_staff.chris_b
    john_doe = setup_staff.john_doe
    appn_greenhouse = setup_facility.appn_greenhouse
    inrae_field = setup_facility.inrae_field

    barley_response = await get_experiment_fixture(
        data=BARLEY_EXPERIMENT,
        study=first_study,
        experiment_type=barley_type,
        staffs=[step_w.staff_response, chris_b.staff_response],
        facilities=[appn_greenhouse.facility_response],
        test_client=test_client,
    )
    maize_response = await get_experiment_fixture(
        data=MAIZE_EXPERIMENT,
        study=first_study,
        experiment_type=maize_type,
        staffs=[john_doe.staff_response],
        facilities=[inrae_field.facility_response],
        test_client=test_client,
    )

    yield AllExperimentFixtureResponse(
        maize=maize_response,
        barley=barley_response,
        study_response=setup_study,
        experiment_type_response=setup_experiment_type,
        facility_response=setup_facility,
        staff_response=setup_staff,
    )
    await delete_fixture(PATH, barley_response.experiment_response.json()["id"], test_client)
    await delete_fixture(PATH, maize_response.experiment_response.json()["id"], test_client)


@pytest.fixture(scope="function")
async def update_experiment(
    setup_experiment: AllExperimentFixtureResponse, test_client: AsyncTestClient
) -> AsyncGenerator[AllExperimentFixtureResponse, None]:
    all_responses = setup_experiment
    john_doe = all_responses.staff_response.john_doe
    inrae_field = all_responses.facility_response.inrae_field
    maize_type = all_responses.experiment_type_response.maize
    maize_study = all_responses.study_response.maize
    maize_response = await get_experiment_fixture(
        data=MAIZE_EXPERIMENT,
        study=maize_study.study_response,
        experiment_type=maize_type,
        staffs=[john_doe.staff_response],
        facilities=[inrae_field.facility_response],
        test_client=test_client,
        id=all_responses.maize.experiment_response.json()["id"],
    )
    all_responses.maize = maize_response
    yield all_responses
