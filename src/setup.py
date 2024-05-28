import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.model import Base
from tests.router.institution.fixture import ANU, APPN, INRAE, RESEARCH_INSTITUTE, TPA, UMR, UNIVERSITY, UOA, UPARIS
from tests.router.investigation.fixture import BARLEY_PROJECT_INVESTIGATION, FIRST_PROJECT, MAIZE_PROJECT_INVESTIGATION
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

        await session.commit()

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(async_main())
