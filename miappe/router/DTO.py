from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig

from miappe.model import Device, Vocabulary, Method


class DeviceReadDTO(SQLAlchemyDTO[Device]):
    config = SQLAlchemyDTOConfig(
        exclude={"device_type.description",
                 "device_type.namespace",
                 "device_type.created_at",
                 "device_type.updated_at",
                 "device_type.external_reference",
                 "device_type.relationship_type",
                 "device_type.symbol",
                 "device_type.id",
                 "method"})


class DeviceWriteDTO(SQLAlchemyDTO[Device]):
    config = SQLAlchemyDTOConfig(exclude={
        "id",
        "device_type",
        "created_at",
        "updated_at",
        "method"})


class VocabularyReadDTO(SQLAlchemyDTO[Vocabulary]):
    config = SQLAlchemyDTOConfig(exclude={"device", "method"})


class VocabularyWriteDTO(SQLAlchemyDTO[Vocabulary]):
    config = SQLAlchemyDTOConfig(exclude={"id", "device", "method"})


class MethodReadDTO(SQLAlchemyDTO[Method]):
    config = SQLAlchemyDTOConfig(exclude={"id", "device", "method_type"})


class MethodWriteDTO(SQLAlchemyDTO[Method]):
    config = SQLAlchemyDTOConfig(exclude={"id", "device", "method_type"})
