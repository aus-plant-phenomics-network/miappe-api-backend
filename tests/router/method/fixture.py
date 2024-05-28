from collections.abc import AsyncGenerator
from dataclasses import dataclass
from uuid import UUID

import pytest
from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.method import Method
from src.model.vocabulary import Vocabulary
from tests.helpers import delete_fixture, post_fixture, put_fixture
from tests.router.device.fixture import DeviceResponse


@dataclass
class MethodReferenceResponse:
    day_to_anthesis: Response
    projected_shoot_area: Response


@dataclass
class MethodResponse:
    method_reference_response: Response
    method_response: Response
    device_response: Response | None = None


@dataclass
class AllMethodFixtureResponse:
    day_to_anthesis: MethodResponse
    projected_shoot_area: MethodResponse
    method_reference: MethodReferenceResponse


PATH = "method"
DAY_TO_ANTHESIS_REF = Vocabulary(
    title="Days to Anthesis",
    accession_number="CO_322:0000189",
    external_reference="http://doi.org/10.2134/agronmonogr31.c2",
)
PROJECTED_SHOOT_AREA_REF = Vocabulary(
    title="Calculated Projected Shoot Area", external_reference="https://doi.org/10.1186/s13007-020-00577-6"
)
DAY_TO_ANTHESIS_METHOD = Method(
    name="Growing degree days to anthesis",
    description="Days to anthesis for male flowering "
    "was measured in thermal time (GDD: growing degree-days) "
    "according to Ritchie J, NeSmith D (1991;Temperature and crop development. "
    "Modeling plant and soil systems American Society of Agronomy Madison, Wisconsin USA) with TBASE=8°C and T0=30°C."
    "Plant height was measured at 5 years with a ruler, one year after Botritis inoculation.",
)
PROJECTED_SHOOT_AREA_METHOD = Method(
    name="calculated projected shoot area using camera images",
    description="Calculated as the sum of the number of plant pixels from 3 camera views (LemnaTec Scanalyzer 3D) "
    "comprising two side views and a view from above. The imaging data was prepared using the SET method "
    "check reference for the computations.",
)


async def get_method_fixture(
    data: Method,
    reference: Response,
    test_client: AsyncTestClient,
    id: UUID | None = None,
    device: Response | None = None,
) -> MethodResponse:
    method_reference_id = reference.json()["id"]
    send_data = Method(method_reference_id=method_reference_id, **data.to_dict())
    if id is None:
        response = await post_fixture(PATH, send_data, test_client)
    else:
        response = await put_fixture(PATH, send_data, test_client, id)
    if device:
        return MethodResponse(method_reference_response=reference, method_response=response, device_response=device)
    return MethodResponse(method_reference_response=reference, method_response=response)


@pytest.fixture(scope="function")
async def setup_method_reference(test_client: AsyncTestClient) -> AsyncGenerator[MethodReferenceResponse, None]:
    day_to_anthesis = await post_fixture("vocabulary", DAY_TO_ANTHESIS_REF, test_client)
    projected_shoot_area = await post_fixture("vocabulary", PROJECTED_SHOOT_AREA_REF, test_client)
    yield MethodReferenceResponse(day_to_anthesis=day_to_anthesis, projected_shoot_area=projected_shoot_area)
    await delete_fixture("vocabulary", day_to_anthesis.json()["id"], test_client)
    await delete_fixture("vocabulary", projected_shoot_area.json()["id"], test_client)


@pytest.fixture(scope="function")
async def setup_method(
    setup_method_reference: MethodReferenceResponse, setup_device: DeviceResponse, test_client: AsyncTestClient
) -> AsyncGenerator[AllMethodFixtureResponse, None]:
    method = setup_method_reference
    day_to_anthesis = await get_method_fixture(DAY_TO_ANTHESIS_METHOD, method.day_to_anthesis, test_client)
    projected_shoot_area = await get_method_fixture(
        PROJECTED_SHOOT_AREA_METHOD, method.projected_shoot_area, test_client, None, setup_device.device_response
    )
    yield AllMethodFixtureResponse(
        day_to_anthesis=day_to_anthesis, projected_shoot_area=projected_shoot_area, method_reference=method
    )
    await delete_fixture(PATH, day_to_anthesis.method_response.json()["id"], test_client)
    await delete_fixture(PATH, projected_shoot_area.method_response.json()["id"], test_client)
