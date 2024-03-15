from typing import TYPE_CHECKING, Generic, TypeVar, Any
from uuid import UUID

from litestar import Controller, get, put, post, delete, Router
from litestar.di import Provide
from sqlalchemy.orm import DeclarativeBase

from miappe.router.utils.CRUD import (
    read_item_by_id,
    create_item,
    delete_item,
    update_item,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


T = TypeVar("T", bound=DeclarativeBase)


class GenericController(Controller, Generic[T]):
    model_type: type[T]

    def __class_getitem__(cls, model_type: type[T]) -> type:
        return type(
            f"Controller[{model_type.__name__}]", (cls,), {"model_type": model_type}
        )

    def __init__(self, owner: Router):
        super().__init__(owner)
        self.signature_namespace[T.__name__] = self.model_type  # type: ignore
        self.dependencies = self.dependencies if self.dependencies else {}
        self.dependencies["table"] = Provide(self.get_table)  # type: ignore

    async def get_table(self) -> type[T]:
        return self.model_type


class BaseController(GenericController[T]):
    @get("/{id:uuid}")
    async def _get_item_by_id(
        self, table: Any, transaction: "AsyncSession", id: UUID
    ) -> T.__name__:
        return await read_item_by_id(session=transaction, table=table, id=id)

    @post()
    async def _create_item(
        self, transaction: "AsyncSession", data: T.__name__
    ) -> T.__name__:
        return await create_item(session=transaction, data=data)

    @put("/{id:uuid}")
    async def _update_item(
        self, table: Any, transaction: "AsyncSession", id: UUID, data: T.__name__
    ) -> T.__name__:
        result = await update_item(session=transaction, id=id, data=data, table=table)
        return result

    @delete("/{id:uuid}")
    async def _delete_item(
        self, table: Any, transaction: "AsyncSession", id: UUID
    ) -> None:
        await delete_item(session=transaction, id=id, table=table)
