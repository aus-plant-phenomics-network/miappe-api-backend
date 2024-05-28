import datetime
from typing import Any, Literal
from uuid import UUID

from httpx import Response
from litestar.testing import AsyncTestClient

from src.model.base import Serialisable


def serialise_datetime(obj: Any) -> str:
    if isinstance(obj, datetime.datetime):
        return obj.strftime("%Y-%m-%d")
    return str(obj)


ScopeValue = Literal["function", "module", "class", "package"]


def snake_to_camel(snake_str: str) -> str:
    # Split the snake_case string into words
    components = snake_str.split("_")
    # Capitalize the first letter of each word except the first one and join them together
    return components[0] + "".join(x.title() for x in components[1:])


def serialise_data(data: dict[str, Any] | Serialisable) -> dict[str, Any]:
    dict_data = data if isinstance(data, dict) else data.to_dict()
    new_dict = {}
    for k, v in dict_data.items():
        new_k = snake_to_camel(k)
        if isinstance(v, datetime.datetime):
            new_dict[new_k] = v.strftime("%Y-%m-%dT%H:%M:%S") if k == "updated_at" else v.isoformat()
        else:
            new_dict[new_k] = v
    return new_dict


async def delete_fixture(path: str, id: UUID, client: AsyncTestClient) -> Response:
    return await client.delete(f"{path}/{id}")


async def post_fixture(path: str, data: dict[str, Any] | Serialisable, client: AsyncTestClient) -> Response:
    return await client.post(path, json=serialise_data(data))


async def put_fixture(path: str, data: dict[str, Any] | Serialisable, client: AsyncTestClient, id: UUID) -> Response:
    return await client.put(f"{path}/{id}", json=serialise_data(data))


async def validate_get_exist(path: str, data: dict[str, Any] | Serialisable, client: AsyncTestClient, id: UUID) -> None:
    query = await client.get(f"{path}/{id}")
    assert query.status_code == 200
    query_data = query.json()
    for k, v in serialise_data(data).items():
        assert k in query_data
        if k != "updatedAt":
            assert v == query_data[k]


async def validate_get_not_exist(path: str, client: AsyncTestClient, id: UUID) -> None:
    query = await client.get(f"{path}/{id}")
    assert query.status_code == 404


async def validate_post(
    path: str, data: dict[str, Any] | Serialisable, client: AsyncTestClient, response: Response
) -> None:
    assert response.status_code == 201
    id = response.json()["id"]
    await validate_get_exist(path, data, client, id)


async def validate_put(
    path: str, data: dict[str, Any] | Serialisable, client: AsyncTestClient, response: Response
) -> None:
    assert response.status_code == 200
    id = response.json()["id"]
    await validate_get_exist(path, data, client, id)
