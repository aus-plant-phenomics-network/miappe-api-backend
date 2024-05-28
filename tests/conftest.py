from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from litestar import Litestar
from litestar.testing import AsyncTestClient

from src.helpers import create_db_config, provide_transaction
from src.router import (
    DataFileController,
    DeviceController,
    InstitutionController,
    InvestigationController,
    MethodController,
    StaffController,
    StudyController,
    VocabularyController,
)

pytest_plugins = [
    "tests.router.investigation.fixture",
    "tests.router.study.fixture",
    "tests.router.institution.fixture",
    "tests.router.staff.fixture",
    "tests.router.data_file.fixture",
    "tests.router.method.fixture",
    "tests.router.device.fixture",
]


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
            MethodController,
            DeviceController,
        ],
        dependencies={"transaction": provide_transaction},
        plugins=[SQLAlchemyPlugin(db_config)],
    )
    async with AsyncTestClient(app=app) as client:
        yield client
    p.unlink(missing_ok=True)
