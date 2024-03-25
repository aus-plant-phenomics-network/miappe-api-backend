from typing import TYPE_CHECKING

from src.model import Variable
from tests.helpers import AbstractBaseTestSuite, ResponseValidator

if TYPE_CHECKING:
    from litestar.testing import AsyncTestClient


class TestVariable(AbstractBaseTestSuite[Variable]):
    path = "variable"
    fixture = {"first": {"name": "first"}, "second": {"name": "second"}, "third": {"name": "third"}}
    update_fixture = {
        "first": {"name": "first_variable"},
        "second": {"name": "second_variable"},
        "third": {"name": "third_variable"},
    }
    invalid_create_fixture = {"first": {"name": "first"}, "second": {"name": "second"}, "third": {"name": "third"}}

    async def test_get_item_by_name(self, test_client: "AsyncTestClient") -> None:
        for key, value in self.fixture.items():
            name = value["name"]
            async with test_client as client:
                response = await client.get(self.path, params={"name": name})
                ResponseValidator.validate_return_item_count(1, response)
                ResponseValidator.validate_response_body(response.json()[0], name=name)
