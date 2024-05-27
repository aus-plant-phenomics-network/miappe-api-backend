import asyncio
import datetime
from datetime import UTC
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.model import Base, DataFile, Institution, Investigation, Staff, Study, Vocabulary


async def insert_investigation(async_session: async_sessionmaker[AsyncSession]) -> dict[str, UUID]:
    async with async_session() as session:
        first_investigation = Investigation(title="First Project")
        second_investigation = Investigation(title="Second Project")
        third_investigation = Investigation(title="Third Project")
        session.add_all([first_investigation, second_investigation, third_investigation])
        await session.commit()
        return {
            "First Project": first_investigation.id,
            "Second Project": second_investigation.id,
            "Third Project": third_investigation.id,
        }


async def insert_study(
    async_session: async_sessionmaker[AsyncSession], investigation: dict[str, UUID]
) -> dict[str, UUID]:
    async with async_session() as session:
        first_study = Study(
            title="First Study",
            objective="First Objective",
            start_date=datetime.datetime.now(UTC),
            investigation_id=investigation["First Project"],
        )
        second_study = Study(
            title="Second Study",
            objective="Second Objective",
            start_date=datetime.datetime.now(UTC),
            investigation_id=investigation["First Project"],
        )
        third_study = Study(
            title="Third Study",
            objective="Third Objective",
            start_date=datetime.datetime.now(UTC),
            investigation_id=investigation["Second Project"],
        )
        session.add_all([first_study, second_study, third_study])
        await session.commit()
        return {"First Study": first_study.id, "Second Study": second_study.id, "Third Study": third_study.id}


async def insert_institution_types(async_session: async_sessionmaker[AsyncSession]) -> dict[str, UUID]:
    async with async_session() as session:
        university = Vocabulary(title="Research University", namespace="Research Institution")
        research_department = Vocabulary(title="Research Department", namespace="Research Institution")
        research_institute = Vocabulary(title="Research Institute", namespace="Research Institution")
        session.add_all([university, research_department, research_institute])
        await session.commit()
        return {
            "university": university.id,
            "research_department": research_department.id,
            "research_institute": research_institute.id,
        }


async def insert_institution(
    async_session: async_sessionmaker[AsyncSession], institution_type: dict[str, UUID]
) -> dict[str, UUID]:
    async with async_session() as session:
        uoa = Institution(title="UoA", country="Aus", institution_type_id=institution_type["university"])
        uq = Institution(title="UQ", country="Aus", institution_type_id=institution_type["university"])
        appn = Institution(title="APPN", country="Aus", institution_type_id=institution_type["research_institute"])
        appn.parents.append(uoa)
        tpa = Institution(title="TPA", country="Aus", institution_type_id=institution_type["research_department"])
        tpa.parents.extend([uoa, appn])
        session.add_all([uoa, uq, appn, tpa])
        await session.commit()
        return {"uoa": uoa.id, "uq": uq.id, "appn": appn.id, "tpa": tpa.id}


async def insert_data_file(
    async_session: async_sessionmaker[AsyncSession], study_id: dict[str, UUID]
) -> dict[str, UUID]:
    async with async_session() as session:
        first_study_ = await session.execute(select(Study).where(Study.id == study_id["First Study"]))
        first_study = first_study_.scalars().one()
        second_study_ = await session.execute(select(Study).where(Study.id == study_id["Second Study"]))
        second_study = second_study_.scalars().one()
        data_file_item = DataFile(
            title="images",
            data_file_description="barley images",
            data_file_link="google.com",
            data_file_version="1.0.0",
        )
        data_file_item.studies = [first_study, second_study]
        session.add(data_file_item)
        await session.commit()
        return {"datafile": data_file_item.id}


async def insert_staff(
    async_session: async_sessionmaker[AsyncSession], institution_id: dict[str, UUID]
) -> dict[str, UUID]:
    async with async_session() as session:
        uoa_ = await session.execute(select(Institution).where(Institution.id == institution_id["uoa"]))
        uoa = uoa_.scalars().one()
        appn_ = await session.execute(select(Institution).where(Institution.id == institution_id["appn"]))
        appn = appn_.scalars().one()
        staff_item = Staff(
            title="John Doe",
            role="SWE",
        )
        staff_item.institutions = [appn, uoa]
        session.add(staff_item)
        await session.commit()
        return {"staff": staff_item.id}


async def async_main() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///db.sqlite", echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    investigation_id = await insert_investigation(async_session)
    institution_type = await insert_institution_types(async_session)
    study_id = await insert_study(async_session, investigation_id)
    institution_id = await insert_institution(async_session, institution_type)
    _ = await insert_data_file(async_session, study_id)
    _ = await insert_staff(async_session, institution_id)

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(async_main())
