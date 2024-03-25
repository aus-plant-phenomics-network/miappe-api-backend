from typing import TYPE_CHECKING

from src.model import Vocabulary
from tests.helpers import AbstractBaseTestSuite, ResponseValidator

if TYPE_CHECKING:
    from litestar.testing import AsyncTestClient


class TestVocabulary(AbstractBaseTestSuite[Vocabulary]):
    path = "vocabulary"
    fixture = {"first": {"name": "first"}, "second": {"name": "second"}, "third": {"name": "third"}}
    update_fixture = {
        "first": {"name": "first_vocabulary"},
        "second": {"name": "second_vocabulary"},
        "third": {"name": "third_vocabulary"},
    }
    invalid_create_fixture = {"first": {"name": "first"}, "second": {"name": "second"}, "third": {"name": "third"}}

    async def test_get_item_by_name(self, test_client: "AsyncTestClient") -> None:
        for key, value in self.fixture.items():
            name = value["name"]
            async with test_client as client:
                response = await client.get(self.path, params={"name": name})
                ResponseValidator.validate_return_item_count(1, response)
                ResponseValidator.validate_response_body(response.json()[0], name=name)
