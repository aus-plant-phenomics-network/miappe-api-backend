import asyncio
import datetime
from datetime import UTC
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.model import Base, Investigation, Study


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


async def async_main() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///db.sqlite", echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    investigation_id = await insert_investigation(async_session)
    await insert_study(async_session, investigation_id)

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(async_main())
