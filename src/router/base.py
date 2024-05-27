from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Generic, TypeVar, cast
from uuid import UUID

from litestar import Controller, Router, delete, get, post, put
from litestar.di import Provide
from sqlalchemy import delete as remove
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, selectinload

__all__ = (
    "BaseController",
    "GenericController",
    "delete_item",
    "read_item_by_id",
    "read_items_by_attrs",
    "update_item",
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.model.base import Base

T = TypeVar("T", bound=DeclarativeBase)


async def read_items_by_attrs(
    session: "AsyncSession",
    table: type[Any],
    selectinload_attrs: list[Any] | None = None,
    id: UUID | list[UUID] | None = None,
    **kwargs: Any,
) -> Sequence[Any]:
    stmt = select(table)
    if selectinload_attrs:
        for attr in selectinload_attrs:
            stmt = stmt.options(selectinload(attr))
    if id:
        processed_id = [id] if isinstance(id, UUID) else id
        stmt = stmt.where(table.__table__.c["id"].in_(processed_id))
    for attr, value in kwargs.items():
        if value is not None:
            stmt = stmt.where(table.__table__.c[attr] == value)
    result = await session.execute(stmt)
    return result.scalars().all()


async def read_item_by_id(
    session: "AsyncSession",
    table: type[Any],
    id: "UUID",
    selectinload_attrs: list[Any] | None = None,
) -> Any:
    stmt = select(table).where(table.__table__.c.id == id)
    if selectinload_attrs:
        for attr in selectinload_attrs:
            stmt = stmt.options(selectinload(attr))
    result = await session.execute(stmt)
    return result.scalars().one()


async def update_item(
    session: "AsyncSession",
    id: "UUID",
    data: "Base",
    table: type[Any],
) -> "Any":
    data_dict = data.to_dict()
    result = await read_item_by_id(session=session, table=table, id=id)
    for attr, value in data_dict.items():
        setattr(result, attr, value)
    return result


async def delete_item(session: "AsyncSession", id: "UUID", table: type[Any]) -> Any:
    stmt = remove(table).where(table.__table__.c.id == id)
    await session.execute(stmt)


class GenericController(Controller, Generic[T]):
    model_type: type[T]

    def __class_getitem__(cls, model_type: type[T]) -> type:
        return type(f"Controller[{model_type.__name__}]", (cls,), {"model_type": model_type})

    def __init__(self, owner: Router):
        super().__init__(owner)
        self.signature_namespace[T.__name__] = self.model_type  # type: ignore[misc]
        self.dependencies = self.dependencies if self.dependencies else {}
        self.dependencies["table"] = Provide(self.get_table)  # type: ignore[index]

    async def get_table(self) -> type[T]:
        return self.model_type


class BaseController(GenericController[T]):
    @get()
    async def get_items(
        self,
        table: Any,
        transaction: "AsyncSession",
        title: str | None,
        id: UUID | list[UUID] | None = None,
        **kwargs: Any,
    ) -> Sequence[T.__name__]:
        return cast(
            Sequence[T],
            await read_items_by_attrs(transaction, table, title=title, id=id, **kwargs),
        )

    @get("/{id:uuid}")
    async def get_item_by_id(
        self,
        table: Any,
        transaction: "AsyncSession",
        id: UUID,
    ) -> T.__name__:
        return cast(
            T,
            await read_item_by_id(session=transaction, table=table, id=id),
        )

    @post()
    async def create_item(
        self,
        transaction: "AsyncSession",
        table: Any,
        data: T.__name__,  # type: ignore[name-defined]
    ) -> T.__name__:  # type: ignore[name-defined]
        transaction.add(data)
        await transaction.flush()
        return await read_item_by_id(transaction, table, data.id)

    @put("/{id:uuid}")
    async def update_item(
        self,
        table: Any,
        transaction: "AsyncSession",
        id: UUID,
        data: T.__name__,  # type: ignore[name-defined]
    ) -> T.__name__:  # type: ignore[name-defined]
        return await update_item(session=transaction, id=id, data=data, table=table)

    @delete("/{id:uuid}")
    async def delete_item(self, table: Any, transaction: "AsyncSession", id: UUID) -> None:
        await delete_item(session=transaction, id=id, table=table)
