from collections.abc import AsyncGenerator
from dataclasses import dataclass
from uuid import UUID

import pytest
from httpx import Response
from litestar.testing import AsyncTestClient

from src.model import ObservationUnit, Vocabulary
from src.model.observation_unit import ObservationUnitDataclass
from tests.helpers import delete_fixture, post_fixture, put_fixture
from tests.router.biological_material.fixture import AllBiologicalMaterialFixtureResponse
from tests.router.experimental_factor.fixture import AllExperimentalFactorFixtureResponse
from tests.router.facility.fixture import AllFacilityFixtureResponse
from tests.router.study.fixture import AllStudyFixtureResponse


@dataclass
class ObservationUnitTypeResponse:
    plant: Response
    plot: Response


@dataclass
class ObservationUnitResponse:
    observation_unit_response: Response
    observation_unit_type_response: Response
    biological_material_response: Response
    experimental_factor_response: list[Response]
    study_response: list[Response]
    parent_response: list[Response]
    facility_response: Response | None = None


@dataclass
class AllObservationUnitFixtureResponse:
    plot_894: ObservationUnitResponse
    plant_061439: ObservationUnitResponse
    plant_061440: ObservationUnitResponse
    study_response: AllStudyFixtureResponse
    biological_material_response: AllBiologicalMaterialFixtureResponse
    facility_response: AllFacilityFixtureResponse
    experimental_factor_response: AllExperimentalFactorFixtureResponse
    observation_unit_type_response: ObservationUnitTypeResponse


PATH = "observationUnit"
PLOT_TYPE = Vocabulary(title="plot", accession_number="Biosamples:SAMEA4202911")
PLANT_TYPE = Vocabulary(title="plant")
PLOT_894 = ObservationUnit(title="894", location="latitude:+2.341; row:4 ; X:3; Y:6; Xm:35; Ym:65; block:1; plot:894")
PLANT_061439 = ObservationUnit(title="061439", location="smarthouse:SW, Lane:4, Position:5")
PLANT_061440 = ObservationUnit(title="061439", location="smarthouse:SW, Lane:4, Position:6")


async def get_observation_unit_fixture(
    observation_unit_type: Response,
    data: ObservationUnit,
    parents: list[Response],
    studies: list[Response],
    experimental_factor: list[Response],
    biological_material: Response,
    test_client: AsyncTestClient,
    id: UUID | None = None,
    facility: Response | None = None,
) -> ObservationUnitResponse:
    observation_unit_type_id = observation_unit_type.json()["id"]
    parent_id = [item.json()["id"] for item in parents]
    study_id = [item.json()["id"] for item in studies]
    experimental_factor_id = [item.json()["id"] for item in experimental_factor]
    facility_id = facility.json()["id"] if facility else None
    biological_material_id = biological_material.json()["id"] if biological_material else None
    parsed_data = data.to_dict()
    post_data = ObservationUnitDataclass(
        facility_id=facility_id,
        observation_unit_type_id=observation_unit_type_id,
        parent_id=parent_id,
        study_id=study_id,
        biological_material_id=biological_material_id,
        experimental_factor_id=experimental_factor_id,
        **parsed_data,
    )
    if id is None:
        post_data.updated_at = None
        response = await post_fixture(PATH, post_data, test_client)
    else:
        response = await put_fixture(PATH, post_data, test_client, id)
    return ObservationUnitResponse(
        observation_unit_response=response,
        parent_response=parents,
        observation_unit_type_response=observation_unit_type,
        biological_material_response=biological_material,
        experimental_factor_response=experimental_factor,
        study_response=studies,
        facility_response=facility,
    )


@pytest.fixture(scope="function")
async def setup_observation_unit_type(
    test_client: AsyncTestClient,
) -> AsyncGenerator[ObservationUnitTypeResponse, None]:
    PATH = "vocabulary"
    plot = await post_fixture(PATH, PLOT_TYPE, test_client)
    plant = await post_fixture(PATH, PLANT_TYPE, test_client)
    yield ObservationUnitTypeResponse(plant=plant, plot=plot)
    await delete_fixture(PATH, plot.json()["id"], test_client)
    await delete_fixture(PATH, plant.json()["id"], test_client)


@pytest.fixture(scope="function")
async def setup_observation_units(
    setup_study: AllStudyFixtureResponse,
    setup_experimental_factor: AllExperimentalFactorFixtureResponse,
    setup_biological_material: AllBiologicalMaterialFixtureResponse,
    setup_facility: AllFacilityFixtureResponse,
    setup_observation_unit_type: ObservationUnitTypeResponse,
    test_client: AsyncTestClient,
) -> AsyncGenerator[AllObservationUnitFixtureResponse, None]:
    maize_study = setup_study.maize.study_response
    barley_study = setup_study.barley.study_response
    watered = setup_experimental_factor.maize_watering_watered.factor_response
    zn_cc_90 = setup_experimental_factor.barley_zn_exposure_90.factor_response
    zn_cc_0 = setup_experimental_factor.barley_zn_exposure_0.factor_response
    fungal_plus = setup_experimental_factor.barley_fungal_exposure_plus.factor_response
    hordeum = setup_biological_material.hordeum.biological_material_response
    zea = setup_biological_material.zea_mays.biological_material_response
    appn_greenhouse = setup_facility.appn_greenhouse.facility_response
    inrae_field = setup_facility.inrae_field.facility_response
    plot = setup_observation_unit_type.plot
    plant = setup_observation_unit_type.plant

    plot_894 = await get_observation_unit_fixture(
        observation_unit_type=plot,
        data=PLOT_894,
        parents=[],
        studies=[maize_study, barley_study],
        experimental_factor=[watered],
        biological_material=zea,
        test_client=test_client,
        facility=inrae_field,
    )
    plant_061439 = await get_observation_unit_fixture(
        observation_unit_type=plant,
        data=PLANT_061439,
        parents=[],
        studies=[barley_study],
        experimental_factor=[zn_cc_90, fungal_plus],
        biological_material=hordeum,
        test_client=test_client,
        facility=appn_greenhouse,
    )
    plant_061440 = await get_observation_unit_fixture(
        observation_unit_type=plant,
        data=PLANT_061440,
        parents=[],
        studies=[barley_study],
        experimental_factor=[zn_cc_0, fungal_plus],
        biological_material=hordeum,
        test_client=test_client,
        facility=appn_greenhouse,
    )

    yield AllObservationUnitFixtureResponse(
        plot_894=plot_894,
        plant_061439=plant_061439,
        plant_061440=plant_061440,
        study_response=setup_study,
        experimental_factor_response=setup_experimental_factor,
        biological_material_response=setup_biological_material,
        facility_response=setup_facility,
        observation_unit_type_response=setup_observation_unit_type,
    )
    await delete_fixture(PATH, plot_894.observation_unit_response.json()["id"], test_client)
    await delete_fixture(PATH, plant_061439.observation_unit_response.json()["id"], test_client)
    await delete_fixture(PATH, plant_061440.observation_unit_response.json()["id"], test_client)


@pytest.fixture(scope="function")
async def update_observation_unit(
    setup_observation_units: AllObservationUnitFixtureResponse, test_client: AsyncTestClient
) -> AsyncGenerator[AllObservationUnitFixtureResponse, None]:
    all_response = setup_observation_units
    plot_894_id = all_response.plot_894.observation_unit_response.json()["id"]
    plot_894 = await get_observation_unit_fixture(
        observation_unit_type=all_response.observation_unit_type_response.plot,
        data=PLOT_894,
        parents=[],
        studies=[all_response.study_response.maize.study_response],
        experimental_factor=[all_response.experimental_factor_response.maize_watering_watered.factor_response],
        biological_material=all_response.biological_material_response.zea_mays.biological_material_response,
        test_client=test_client,
        id=plot_894_id,
        facility=all_response.facility_response.inrae_field.facility_response,
    )
    all_response.plot_894 = plot_894
    yield all_response
