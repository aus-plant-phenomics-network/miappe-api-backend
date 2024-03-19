from miappe.model import Device

from tests.helpers import AbstractBaseTestSuite, ResponseValidator


class TestDevice(AbstractBaseTestSuite[Device]):
    path = "device"
    fixture = {"first": {"name": "first"},
               "second": {"name": "second"},
               "third": {"name": "third"}}
    update_fixture = {"first": {"name": "first_device"},
                      "second": {"name": "second_device"},
                      "third": {"name": "third_device"}}
    invalid_create_fixture = {"first": {"name": "first"},
                              "second": {"name": "second"},
                              "third": {"name": "third"}}

    async def test_get_item_by_name(self, test_client):
        for key, value in self.fixture.items():
            name = value['name']
            async with test_client as client:
                response = await client.get(self.path, params={"name": name})
                ResponseValidator.validate_return_item_count(1, response)
                ResponseValidator.validate_response_body(response.json()[0], name=name)
