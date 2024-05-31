from collections.abc import AsyncGenerator
from dataclasses import dataclass
from uuid import UUID

import pytest
from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.observed_variable import ObservedVariable, ObservedVariableDataclass
from src.model.vocabulary import Vocabulary
from tests.helpers import delete_fixture, post_fixture, put_fixture
from tests.router.method.fixture import AllMethodFixtureResponse
from tests.router.study.fixture import AllStudyFixtureResponse
from tests.router.unit.fixture import AllUnitFixtureResponse


@dataclass
class ObservedVariableResponse:
    trait_response: Response
    observed_variable_response: Response
    study_response: list[Response]
    method_response: Response
    unit_response: Response


@dataclass
class VariableTraitResponse:
    anthesis: Response
    reproductive_growth_time: Response
    projected_shoot_area: Response
    zn_concentration: Response


@dataclass
class AllObservedVariableFixtureResponse:
    anthesis: ObservedVariableResponse
    reproductive_growth_time: ObservedVariableResponse
    projected_shoot_area: ObservedVariableResponse
    zn_concentration: ObservedVariableResponse
    trait_response: VariableTraitResponse
    study_response: AllStudyFixtureResponse
    method_response: AllMethodFixtureResponse
    unit_response: AllUnitFixtureResponse


PATH = "observedVariable"
ANTHESIS_TRAIT = Vocabulary(title="Anthesis time", accession_number="CO_322:0000030")
REPRODUCTIVE_GROWTH_TIME_TRAIT = Vocabulary(title="Reproductive growth time", accession_number="TO:0000366")
PROJECTED_SHOOT_AREA_TRAIT = Vocabulary(title="Projected shoot area")
ZN_CONCENTRATION_TRAIT = Vocabulary(title="Zn concentration", accession_number="CDNO_0200170")

ANTHESIS_VARIABLE = ObservedVariable(
    title="Ant_Cmp_Cday",
    description="Anthesis computed in growing degree days",
    time_interval="day",
)
REPRODUCTIVE_GROWTH_TIME_VARIABLE = ObservedVariable(
    title="Reproductive Growth Time",
    description="Reproductive growth time",
    time_interval="day",
)
PROJECTED_SHOOT_AREA_VARIABLE = ObservedVariable(title="PSA_img_kpixels")
ZN_CONCENTRATION_VARIABLE = ObservedVariable(title="Zn_conc")


async def get_observed_variable_fixture(
    data: ObservedVariable,
    studies: list[Response],
    method: Response,
    trait: Response,
    unit: Response,
    test_client: AsyncTestClient,
    id: UUID | None = None,
) -> ObservedVariableResponse:
    study_id = [item.json()["id"] for item in studies]
    method_id = method.json()["id"]
    trait_reference_id = trait.json()["id"]
    unit_id = unit.json()["id"]
    send_data = ObservedVariableDataclass(
        method_id=method_id,
        trait_reference_id=trait_reference_id,
        study_id=study_id,
        unit_id=unit_id,
        **data.to_dict(),
    )
    if id is None:
        send_data.updated_at = None
        response = await post_fixture(PATH, send_data, test_client)
    else:
        response = await put_fixture(PATH, send_data, test_client, id)
    return ObservedVariableResponse(
        study_response=studies,
        method_response=method,
        unit_response=unit,
        trait_response=trait,
        observed_variable_response=response,
    )


@pytest.fixture(scope="function")
async def setup_trait(test_client: AsyncTestClient) -> AsyncGenerator[VariableTraitResponse, None]:
    PATH = "vocabulary"
    anthesis_trait = await post_fixture(PATH, ANTHESIS_TRAIT, test_client)
    projected_shoot_area_trait = await post_fixture(PATH, PROJECTED_SHOOT_AREA_TRAIT, test_client)
    zn_concentration_trait = await post_fixture(PATH, ZN_CONCENTRATION_TRAIT, test_client)
    reproductive_growth_time_trait = await post_fixture(PATH, REPRODUCTIVE_GROWTH_TIME_TRAIT, test_client)
    yield VariableTraitResponse(
        anthesis=anthesis_trait,
        reproductive_growth_time=reproductive_growth_time_trait,
        projected_shoot_area=projected_shoot_area_trait,
        zn_concentration=zn_concentration_trait,
    )
    await delete_fixture(PATH, anthesis_trait.json()["id"], test_client)
    await delete_fixture(PATH, reproductive_growth_time_trait.json()["id"], test_client)
    await delete_fixture(PATH, projected_shoot_area_trait.json()["id"], test_client)
    await delete_fixture(PATH, zn_concentration_trait.json()["id"], test_client)


@pytest.fixture(scope="function")
async def setup_observed_variable(
    setup_study: AllStudyFixtureResponse,
    setup_method: AllMethodFixtureResponse,
    setup_unit: AllUnitFixtureResponse,
    setup_trait: VariableTraitResponse,
    test_client: AsyncTestClient,
) -> AsyncGenerator[AllObservedVariableFixtureResponse, None]:
    first_study = setup_study.first.study_response
    maize_study = setup_study.maize.study_response
    barley_study = setup_study.maize.study_response

    projected_shoot_area_method = setup_method.projected_shoot_area.method_response
    zn_concentration_method = setup_method.zn_concentration.method_response
    day_to_anthesis_method = setup_method.day_to_anthesis.method_response

    growing_degree_day = setup_unit.degree_day.unit_response
    kilopixel = setup_unit.kilo_pixel.unit_response
    microgram = setup_unit.microgram.unit_response

    anthesis_trait = setup_trait.anthesis
    projected_shoot_area_trait = setup_trait.projected_shoot_area
    zn_concentration_trait = setup_trait.zn_concentration
    reproductive_growth_time_trait = setup_trait.reproductive_growth_time

    anthesis_variable = await get_observed_variable_fixture(
        data=ANTHESIS_VARIABLE,
        studies=[first_study],
        method=day_to_anthesis_method,
        trait=anthesis_trait,
        unit=growing_degree_day,
        test_client=test_client,
    )
    reproductive_growth_time_variable = await get_observed_variable_fixture(
        data=REPRODUCTIVE_GROWTH_TIME_VARIABLE,
        studies=[maize_study],
        method=day_to_anthesis_method,
        trait=reproductive_growth_time_trait,
        unit=growing_degree_day,
        test_client=test_client,
    )
    projected_shoot_area_variable = await get_observed_variable_fixture(
        data=PROJECTED_SHOOT_AREA_VARIABLE,
        studies=[barley_study],
        method=projected_shoot_area_method,
        trait=projected_shoot_area_trait,
        unit=kilopixel,
        test_client=test_client,
    )
    zn_concentration_variable = await get_observed_variable_fixture(
        data=ZN_CONCENTRATION_VARIABLE,
        studies=[barley_study],
        method=zn_concentration_method,
        trait=zn_concentration_trait,
        unit=microgram,
        test_client=test_client,
    )

    yield AllObservedVariableFixtureResponse(
        reproductive_growth_time=reproductive_growth_time_variable,
        projected_shoot_area=projected_shoot_area_variable,
        zn_concentration=zn_concentration_variable,
        anthesis=anthesis_variable,
        study_response=setup_study,
        method_response=setup_method,
        trait_response=setup_trait,
        unit_response=setup_unit,
    )


@pytest.fixture(scope="function")
async def update_observed_variable(
    setup_observed_variable: AllObservedVariableFixtureResponse, test_client: AsyncTestClient
) -> AsyncGenerator[AllObservedVariableFixtureResponse, None]:
    all_responses = setup_observed_variable
    maize_study = all_responses.study_response.maize.study_response
    anthesis = all_responses.anthesis
    anthesis_response = await get_observed_variable_fixture(
        data=ANTHESIS_VARIABLE,
        studies=[maize_study],
        test_client=test_client,
        id=anthesis.observed_variable_response.json()["id"],
        method=anthesis.method_response,
        trait=anthesis.trait_response,
        unit=anthesis.unit_response,
    )
    all_responses.anthesis = anthesis_response
    yield all_responses
