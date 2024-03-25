from litestar import Litestar
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin

from src.helpers import create_db_config, provide_transaction
from src.router import (
    DeviceController,
    MethodController,
    UnitController,
    VariableController,
    VocabularyController,
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
