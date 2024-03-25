from litestar import Litestar
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin

from src.helpers import provide_transaction, create_db_config
from src.router import (
    VocabularyController,
    DeviceController,
    MethodController,
    UnitController,
    VariableController,
)

db_config = create_db_config("db.sqlite")

app = Litestar(
    [
        DeviceController,
        VocabularyController,
        MethodController,
        UnitController,
        VariableController,
    ],
    dependencies={"transaction": provide_transaction},
    plugins=[SQLAlchemyPlugin(db_config)],
)
