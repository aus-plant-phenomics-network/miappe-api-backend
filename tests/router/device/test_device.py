from dataclasses import dataclass
from uuid import UUID

from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.device import Device
from tests.helpers import validate_post
from tests.router.device.fixture import PATH, SCANALYZER_DEVICE, DeviceResponse


@dataclass
class DeviceFixture:
    id: UUID
    response: Response
    data: Device
    device_type_id: UUID


def get_device_fixture(response: DeviceResponse, data: Device) -> DeviceFixture:
    device_response = response.device_response
    device_type_id = response.device_type_response.json()["id"]
    fixture = Device(device_type_id=device_type_id, **data.to_dict())
    return DeviceFixture(
        id=device_response.json()["id"], response=device_response, data=fixture, device_type_id=device_type_id
    )


async def test_scanalyzer_created(setup_device: DeviceResponse, test_client: AsyncTestClient) -> None:
    fixture = get_device_fixture(setup_device, SCANALYZER_DEVICE)
    await validate_post(PATH, fixture.data, test_client, fixture.response)
