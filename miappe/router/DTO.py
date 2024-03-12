from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig

from miappe.model import Device, Vocabulary


class DeviceReadDTO(SQLAlchemyDTO[Device]):
    config = SQLAlchemyDTOConfig(
        exclude={"device_type.description", "device_type.namespace", "device_type.created_at", "device_type.updated_at",
                 "device_type.external_reference", "device_type.relationship_type", "device_type.symbol", "device_type.id"})


class DeviceWriteDTO(SQLAlchemyDTO[Device]):
    config = SQLAlchemyDTOConfig(exclude={"id", "device_type", "created_at", "updated_at"})


class VocabularyReadDTO(SQLAlchemyDTO[Vocabulary]):
    config = SQLAlchemyDTOConfig(exclude={"device"})


class VocabularyWriteDTO(SQLAlchemyDTO[Vocabulary]):
    config = SQLAlchemyDTOConfig(exclude={"id", "device"})
