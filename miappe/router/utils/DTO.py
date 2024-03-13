from copy import deepcopy
from typing import Any

from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig

from miappe.model import Device, Vocabulary, Method, Unit


class DTOGenerator:
    def __init__(self,
                 table: Any,
                 read_exclude: set | None = None,
                 write_exclude: set | None = None):
        self.table = table
        self.read_exclude = read_exclude if read_exclude is not None else set()
        self.write_exclude = write_exclude if write_exclude is not None else set()

        class GetDTO(SQLAlchemyDTO[table]):
            config = SQLAlchemyDTOConfig(exclude=read_exclude)

        post_exclude = deepcopy(self.write_exclude)
        post_exclude = post_exclude | {"id", "created_at", "updated_at"}

        class PostDTO(SQLAlchemyDTO[table]):
            config = SQLAlchemyDTOConfig(exclude=post_exclude)

        put_exclude = deepcopy(self.write_exclude)
        put_exclude = put_exclude | {"id", "created_at"}

        class PutDTO(SQLAlchemyDTO[table]):
            config = SQLAlchemyDTOConfig(exclude=put_exclude)

        self.read_dto = GetDTO
        self.write_dto = PostDTO
        self.update_dto = PutDTO


DeviceDTO = DTOGenerator(table=Device,
                         read_exclude={"device_type.description",
                                       "device_type.namespace",
                                       "device_type.created_at",
                                       "device_type.updated_at",
                                       "device_type.external_reference",
                                       "device_type.relationship_type",
                                       "device_type.symbol",
                                       "device_type.id",
                                       "method"},
                         write_exclude={"device_type", "method"})

VocabularyDTO = DTOGenerator(table=Vocabulary,
                             read_exclude={"device", "method", "unit"},
                             write_exclude={"device", "method", "unit"})

MethodDTO = DTOGenerator(table=Method,
                         read_exclude={"device",
                                       "method_type.description",
                                       "method_type.namespace",
                                       "method_type.created_at",
                                       "method_type.updated_at",
                                       "method_type.external_reference",
                                       "method_type.relationship_type",
                                       "method_type.symbol",
                                       "method_type.id"
                                       },
                         write_exclude={"device", "method_type"})

UnitDTO = DTOGenerator(table=Unit,
                       read_exclude={
                                     "unit_type.description",
                                     "unit_type.namespace",
                                     "unit_type.created_at",
                                     "unit_type.updated_at",
                                     "unit_type.external_reference",
                                     "unit_type.relationship_type",
                                     "unit_type.symbol",
                                     "unit_type.id",
                                     },
                       write_exclude={"unit_type"})
