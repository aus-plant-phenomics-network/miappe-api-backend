import datetime
from typing import Sequence, TYPE_CHECKING
from typing import Any
from sqlalchemy import select, delete

if TYPE_CHECKING:
    from uuid import UUID
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import DeclarativeBase
    from advanced_alchemy.base import CommonTableAttributes


async def create_item(session: "AsyncSession", data: Any) -> Any:
    session.add(data)
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


async def delete_item(session: "AsyncSession", id: "UUID", table: type[Any]) -> "Any":
    stmt = delete(table).where(table.__table__.c.id == id)
    await session.execute(stmt)
    return
