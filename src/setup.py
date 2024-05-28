import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.model import Base
from tests.router.data_file.fixture import BARLEY_DATA_FILE, MAIZE_DATA_FILE
from tests.router.device.fixture import SCANALYZER_DEVICE, SCANALYZER_TYPE
from tests.router.institution.fixture import ANU, APPN, INRAE, RESEARCH_INSTITUTE, TPA, UMR, UNIVERSITY, UOA, UPARIS
from tests.router.investigation.fixture import BARLEY_PROJECT_INVESTIGATION, FIRST_PROJECT, MAIZE_PROJECT_INVESTIGATION
from tests.router.method.fixture import (
    DAY_TO_ANTHESIS_METHOD,
    DAY_TO_ANTHESIS_REF,
    PROJECTED_SHOOT_AREA_METHOD,
    PROJECTED_SHOOT_AREA_REF,
)
from tests.router.staff.fixture import CHRIS_B, JOHN_DOE, STEP_W
from tests.router.study.fixture import BARLEY_PROJECT_STUDY, FIRST_STUDY, MAIZE_PROJECT_STUDY, SECOND_STUDY


async def async_main() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///db.sqlite", echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # Add investigation
        session.add_all([FIRST_PROJECT, BARLEY_PROJECT_INVESTIGATION, MAIZE_PROJECT_INVESTIGATION])

        # Add study
        FIRST_STUDY.investigation = FIRST_PROJECT
        SECOND_STUDY.investigation = FIRST_PROJECT
        BARLEY_PROJECT_STUDY.investigation = BARLEY_PROJECT_INVESTIGATION
        MAIZE_PROJECT_STUDY.investigation = MAIZE_PROJECT_INVESTIGATION
        session.add_all([FIRST_STUDY, SECOND_STUDY, BARLEY_PROJECT_STUDY, MAIZE_PROJECT_STUDY])

        # Add institution
        ANU.institution_type = UNIVERSITY
        UOA.institution_type = UNIVERSITY
        APPN.institution_type = RESEARCH_INSTITUTE
        APPN.parents = [ANU, UOA]
        TPA.institution_type = RESEARCH_INSTITUTE
        TPA.parents = [UOA, APPN]
        UPARIS.institution_type = UNIVERSITY
        INRAE.institution_type = RESEARCH_INSTITUTE
        UMR.institution_type = RESEARCH_INSTITUTE
        UMR.parents = [INRAE, UPARIS]
        session.add_all([ANU, APPN, INRAE, RESEARCH_INSTITUTE, TPA, UMR, UNIVERSITY, UOA, UPARIS])

        # Add staff
        CHRIS_B.institutions = [UOA, TPA]
        STEP_W.institutions = [APPN]
        JOHN_DOE.institutions = [UOA]
        session.add_all([CHRIS_B, STEP_W, JOHN_DOE])

        # Add data file
        BARLEY_DATA_FILE.studies = [BARLEY_PROJECT_STUDY]
        MAIZE_DATA_FILE.studies = [MAIZE_PROJECT_STUDY]
        session.add_all([BARLEY_DATA_FILE, MAIZE_DATA_FILE])

        # Add device
        SCANALYZER_DEVICE.device_type = SCANALYZER_TYPE
        session.add_all([SCANALYZER_TYPE, SCANALYZER_DEVICE])

        # Add method
        PROJECTED_SHOOT_AREA_METHOD.method_reference = PROJECTED_SHOOT_AREA_REF
        PROJECTED_SHOOT_AREA_METHOD.device = SCANALYZER_DEVICE
        DAY_TO_ANTHESIS_METHOD.method_reference = DAY_TO_ANTHESIS_REF
        session.add_all([PROJECTED_SHOOT_AREA_METHOD, DAY_TO_ANTHESIS_METHOD])

        await session.commit()

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(async_main())
