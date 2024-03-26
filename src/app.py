from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyPlugin

from src.helpers import create_db_config
from src.helpers import provide_transaction
from src.router import (
    DeviceController, VocabularyController, MethodController, UnitController, VariableController
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
