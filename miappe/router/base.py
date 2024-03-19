import datetime
from typing import Any, Generic, Sequence, TYPE_CHECKING, TypeVar
from uuid import UUID

from litestar import Controller, Router, delete, get, post, put
from litestar.di import Provide
from sqlalchemy import delete as remove
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase

if TYPE_CHECKING:
    from litestar.contrib.sqlalchemy.base import CommonTableAttributes
    from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=DeclarativeBase)


async def create_item(session: "AsyncSession", data: Any) -> Any:
    session.add(data)
    await session.flush()
    return data


async def read_items_by_attrs(
        session: "AsyncSession", table: type[Any], **kwargs
) -> Sequence[Any]:
    stmt = select(table)
    for attr, value in kwargs.items():
        if value:
            stmt = stmt.where(table.__table__.c[attr] == value)
    result = await session.execute(stmt)
    return result.scalars().all()


async def read_item_by_id(session: "AsyncSession", table: type[Any], id: "UUID") -> Any:
    stmt = select(table).where(table.__table__.c.id == id)
    result = await session.execute(stmt)
    return result.scalars().one()


async def update_item(
        session: "AsyncSession",
        id: "UUID",
        data: "CommonTableAttributes",
        table: type[Any],
) -> "Any":
    data_ = {k: v for k, v in data.to_dict().items() if v}
    data_["updated_at"] = datetime.datetime.now(datetime.timezone.utc)
    result = await read_item_by_id(session=session, table=table, id=id)
    for attr, value in data_.items():
        setattr(result, attr, value)
    return result


async def delete_item(session: "AsyncSession", id: "UUID", table: type[Any]) -> Any:
    stmt = remove(table).where(table.__table__.c.id == id)
    await session.execute(stmt)


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
    async def get_item_by_id(
            self, table: Any, transaction: "AsyncSession", id: UUID
    ) -> T.__name__:  # type: ignore[name-defined]
        return await read_item_by_id(session=transaction, table=table, id=id)

    @post()
    async def create_item(
            self, transaction: "AsyncSession", data: T.__name__
            # type: ignore[name-defined]
    ) -> T.__name__:  # type: ignore[name-defined]
        return await create_item(session=transaction, data=data)

    @put("/{id:uuid}")
    async def update_item(
            self, table: Any, transaction: "AsyncSession", id: UUID,
            data: T.__name__  # type: ignore[name-defined]
    ) -> T.__name__:  # type: ignore[name-defined]
        result = await update_item(session=transaction, id=id, data=data, table=table)
        return result

    @delete("/{id:uuid}")
    async def delete_item(
            self, table: Any, transaction: "AsyncSession", id: UUID
    ) -> None:
        await delete_item(session=transaction, id=id, table=table)
