from collections.abc import AsyncGenerator
from dataclasses import dataclass

import pytest
from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.device import Device
from src.model.vocabulary import Vocabulary
from tests.helpers import delete_fixture, post_fixture

PATH = "device"


@dataclass
class DeviceResponse:
    device_response: Response
    device_type_response: Response


SCANALYZER_TYPE = Vocabulary(
    title="Scanalyzer",
    external_reference="https://www.environmental-expert.com/products/model-gl622-laser-transmitter-with-dual-grade-310836",
)
SCANALYZER_DEVICE = Device(name="Scanalyzer-3D Lemnatec", brand="Lemnatec")


@pytest.fixture(scope="function")
async def setup_device(test_client: AsyncTestClient) -> AsyncGenerator[DeviceResponse, None]:
    scanalyzer_type = await post_fixture("vocabulary", SCANALYZER_TYPE, test_client)
    scanalyzer_type_id = scanalyzer_type.json()["id"]
    device = Device(device_type_id=scanalyzer_type_id, **SCANALYZER_DEVICE.to_dict())
    device_response = await post_fixture(PATH, device, test_client)
    yield DeviceResponse(device_type_response=scanalyzer_type, device_response=device_response)
    await delete_fixture("vocabulary", scanalyzer_type.json()["id"], test_client)
    await delete_fixture(PATH, device_response.json()["id"], test_client)
