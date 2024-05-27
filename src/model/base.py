import abc
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any, Protocol
from uuid import UUID, uuid4

from advanced_alchemy.base import CommonTableAttributes
from advanced_alchemy.types import DateTimeUTC
from litestar.dto import dto_field
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

__all__ = ("Base", "BaseDataclass")


class Serialisable(Protocol):
    def to_dict(self, exclude: set[str] | None = None) -> dict[str, Any]:
        return {}


class Base(CommonTableAttributes, DeclarativeBase):
    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True, info=dto_field("read-only"))
    title: Mapped[str] = mapped_column(nullable=False, unique=True)

    # Audit columns - read-only
    created_at: Mapped[datetime] = mapped_column(
        DateTimeUTC(timezone=True),
        default=lambda: datetime.now(UTC),
        info=dto_field("read-only"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTimeUTC(timezone=True),
        default=lambda: datetime.now(UTC),
        info=dto_field("read-only"),
    )

    def to_dict(self, exclude: set[str] | None = None) -> dict[str, Any]:
        data_dict = super().to_dict(exclude)
        data_dict["updated_at"] = datetime.now(UTC)
        return {k: v for k, v in data_dict.items() if v is not None}


@dataclass
class BaseDataclass:
    id: UUID | None
    title: str
    created_at: datetime | None
    updated_at: datetime | None

    def to_dict(self, exclude: set[str] | None = None) -> dict[str, Any]:
        result = {k: v for k, v in asdict(self).items() if v is not None}
        if exclude:
            return {k: v for k, v in result.items() if k not in exclude}
        return result

    @classmethod
    @abc.abstractmethod
    def from_orm(cls, data: Serialisable) -> "BaseDataclass":
        data_dict = data.to_dict()
        return cls(**data_dict)
