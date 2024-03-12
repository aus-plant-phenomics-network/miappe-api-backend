from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig

from miappe.model import Device, Vocabulary


class DeviceReadDTO(SQLAlchemyDTO[Device]):
    config = SQLAlchemyDTOConfig(exclude={"device_type"})


class DeviceWriteDTO(SQLAlchemyDTO[Device]):
    config = SQLAlchemyDTOConfig(exclude={"id", "device_type", "created_at", "updated_at"})


class VocabularyReadDTO(SQLAlchemyDTO[Vocabulary]):
    config = SQLAlchemyDTOConfig(exclude={"device"})


class VocabularyWriteDTO(SQLAlchemyDTO[Vocabulary]):
    config = SQLAlchemyDTOConfig(exclude={"id", "device"})
