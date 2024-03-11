from sqlalchemy.orm import DeclarativeBase
from advanced_alchemy.base import AuditColumns, CommonTableAttributes


class Base(AuditColumns, CommonTableAttributes, DeclarativeBase):
    pass
