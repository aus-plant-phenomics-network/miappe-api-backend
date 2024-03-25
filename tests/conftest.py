from pathlib import Path
from typing import Generator

import pytest
from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from litestar import Litestar
from litestar.testing import AsyncTestClient

from src.helpers import create_db_config, provide_transaction
from src.router import DeviceController, VocabularyController, MethodController, UnitController, VariableController


@pytest.fixture(scope="module")
def test_client() -> Generator[AsyncTestClient, None, None]:
    p = Path("test.sqlite")
    db_config = create_db_config("test.sqlite")
    app = Litestar([
        DeviceController,
        VocabularyController,
        MethodController,
        UnitController,
        VariableController,
    ],
        dependencies={"transaction": provide_transaction},
        plugins=[SQLAlchemyPlugin(db_config)]
    )
    yield AsyncTestClient(app=app)
    p.unlink(missing_ok=True)
