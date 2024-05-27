from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from litestar import Litestar
from litestar.testing import AsyncTestClient

from src.helpers import create_db_config, provide_transaction
from src.router import (
    DataFileController,
    InstitutionController,
    InvestigationController,
    StaffController,
    StudyController,
    VocabularyController,
)


@pytest.fixture(scope="function", autouse=True)
async def test_client() -> AsyncGenerator[AsyncTestClient[Litestar], None]:
    p = Path("test.sqlite")
    db_config = create_db_config("test.sqlite")
    app = Litestar(
        [
            InvestigationController,
            StudyController,
            VocabularyController,
            InstitutionController,
            DataFileController,
            StaffController,
        ],
        dependencies={"transaction": provide_transaction},
        plugins=[SQLAlchemyPlugin(db_config)],
    )
    async with AsyncTestClient(app=app) as client:
        yield client
    p.unlink(missing_ok=True)
