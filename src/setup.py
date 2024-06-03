import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.model import Base
from tests.router.biological_material.fixture import (
    HORDEUM_MATERIAL,
    HORDEUM_REFERENCE,
    ZEA_MAYS_MATERIAL,
    ZEA_MAYS_REFERENCE,
)
from tests.router.data_file.fixture import BARLEY_DATA_FILE, MAIZE_DATA_FILE
from tests.router.device.fixture import SCANALYZER_DEVICE, SCANALYZER_TYPE
from tests.router.environment.fixture import (
    BARLEY_FERTILIZER,
    BARLEY_LIGHT_INTENSITY,
    BARLEY_RELATIVE_HUMIDITY,
    BARLEY_ROOTING_MEDIUM,
    BARLEY_SOWING_DENSITY,
    BARLEY_TEMPERATURE,
    BARLEY_WATERING_EXPOSURE,
    MAIZE_PH,
    MAIZE_ROOTING_MEDIUM,
    MAIZE_SOWING_DENSITY,
)
from tests.router.event.fixture import (
    FERTILIZING_EVENT,
    FERTILIZING_TYPE,
    PLANTING_EVENT,
    PLANTING_TYPE,
    WATERING_EVENT,
    WATERING_TYPE,
)
from tests.router.experiment.fixture import (
    BARLEY_EXPERIMENT,
    BARLEY_EXPERIMENT_TYPE,
    MAIZE_EXPERIMENT,
    MAIZE_EXPERIMENT_TYPE,
)
from tests.router.experimental_factor.fixture import (
    BARLEY_FUNGAL_EXPOSURE_FACTOR_MINUS,
    BARLEY_FUNGAL_EXPOSURE_FACTOR_PLUS,
    BARLEY_FUNGAL_EXPOSURE_TYPE,
    BARLEY_ZN_EXPOSURE_FACTOR_0,
    BARLEY_ZN_EXPOSURE_FACTOR_10,
    BARLEY_ZN_EXPOSURE_FACTOR_40,
    BARLEY_ZN_EXPOSURE_FACTOR_90,
    BARLEY_ZN_EXPOSURE_TYPE,
    MAIZE_WATERING_FACTOR_UNWATERED,
    MAIZE_WATERING_FACTOR_WATERED,
    MAIZE_WATERING_TYPE,
)
from tests.router.facility.fixture import APPN_GREENHOUSE, FIELD_CONDITION_TYPE, GREENHOUSE_TYPE, INRAE_FIELD
from tests.router.institution.fixture import ANU, APPN, INRAE, RESEARCH_INSTITUTE, TPA, UMR, UNIVERSITY, UOA, UPARIS
from tests.router.investigation.fixture import BARLEY_PROJECT_INVESTIGATION, FIRST_PROJECT, MAIZE_PROJECT_INVESTIGATION
from tests.router.method.fixture import (
    DAY_TO_ANTHESIS_METHOD,
    DAY_TO_ANTHESIS_REF,
    PROJECTED_SHOOT_AREA_METHOD,
    PROJECTED_SHOOT_AREA_REF,
    ZN_CONCENTRATION_METHOD,
)
from tests.router.observation_unit.fixture import PLANT_061439, PLANT_061440, PLANT_TYPE, PLOT_894, PLOT_TYPE
from tests.router.observed_variable.fixture import (
    ANTHESIS_TRAIT,
    ANTHESIS_VARIABLE,
    PROJECTED_SHOOT_AREA_TRAIT,
    PROJECTED_SHOOT_AREA_VARIABLE,
    REPRODUCTIVE_GROWTH_TIME_TRAIT,
    REPRODUCTIVE_GROWTH_TIME_VARIABLE,
    ZN_CONCENTRATION_TRAIT,
    ZN_CONCENTRATION_VARIABLE,
)
from tests.router.sample.fixture import (
    CEA_BE00034067,
    LEAFDISC_061439,
    LEAFDISC_061440,
    PO_0006001,
    PO_0007010,
    PO_0025094,
    PO_0025161,
)
from tests.router.staff.fixture import CHRIS_B, JOHN_DOE, STEP_W
from tests.router.study.fixture import BARLEY_PROJECT_STUDY, FIRST_STUDY, MAIZE_PROJECT_STUDY, SECOND_STUDY
from tests.router.unit.fixture import DEGREE_DAY_REF, DEGREE_DAY_UNIT, KILO_PIXEL_UNIT, MICROGRAM_UNIT

__all__ = ("async_main",)


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
        session.add_all([PROJECTED_SHOOT_AREA_METHOD, DAY_TO_ANTHESIS_METHOD, ZN_CONCENTRATION_METHOD])

        # Add unit
        DEGREE_DAY_UNIT.unit_reference = DEGREE_DAY_REF
        session.add_all([DEGREE_DAY_REF, DEGREE_DAY_UNIT, MICROGRAM_UNIT, KILO_PIXEL_UNIT])

        # Add environment variable
        MAIZE_SOWING_DENSITY.studies = [MAIZE_PROJECT_STUDY]
        MAIZE_PH.studies = [MAIZE_PROJECT_STUDY]
        MAIZE_ROOTING_MEDIUM.studies = [MAIZE_PROJECT_STUDY]
        BARLEY_FERTILIZER.studies = [BARLEY_PROJECT_STUDY]
        BARLEY_ROOTING_MEDIUM.studies = [BARLEY_PROJECT_STUDY]
        BARLEY_TEMPERATURE.studies = [BARLEY_PROJECT_STUDY]
        BARLEY_LIGHT_INTENSITY.studies = [BARLEY_PROJECT_STUDY]
        BARLEY_RELATIVE_HUMIDITY.studies = [BARLEY_PROJECT_STUDY]
        BARLEY_SOWING_DENSITY.studies = [BARLEY_PROJECT_STUDY]
        BARLEY_WATERING_EXPOSURE.studies = [BARLEY_PROJECT_STUDY]
        session.add_all(
            [
                BARLEY_FERTILIZER,
                BARLEY_LIGHT_INTENSITY,
                BARLEY_RELATIVE_HUMIDITY,
                BARLEY_ROOTING_MEDIUM,
                BARLEY_SOWING_DENSITY,
                BARLEY_TEMPERATURE,
                BARLEY_WATERING_EXPOSURE,
                MAIZE_PH,
                MAIZE_ROOTING_MEDIUM,
                MAIZE_SOWING_DENSITY,
            ]
        )

        # Add experimental factor
        BARLEY_ZN_EXPOSURE_FACTOR_0.factor_type = BARLEY_ZN_EXPOSURE_TYPE
        BARLEY_ZN_EXPOSURE_FACTOR_0.studies = [BARLEY_PROJECT_STUDY]
        BARLEY_ZN_EXPOSURE_FACTOR_10.factor_type = BARLEY_ZN_EXPOSURE_TYPE
        BARLEY_ZN_EXPOSURE_FACTOR_10.studies = [BARLEY_PROJECT_STUDY]
        BARLEY_ZN_EXPOSURE_FACTOR_40.factor_type = BARLEY_ZN_EXPOSURE_TYPE
        BARLEY_ZN_EXPOSURE_FACTOR_40.studies = [BARLEY_PROJECT_STUDY]
        BARLEY_ZN_EXPOSURE_FACTOR_90.factor_type = BARLEY_ZN_EXPOSURE_TYPE
        BARLEY_ZN_EXPOSURE_FACTOR_90.studies = [BARLEY_PROJECT_STUDY]

        MAIZE_WATERING_FACTOR_WATERED.factor_type = MAIZE_WATERING_TYPE
        MAIZE_WATERING_FACTOR_WATERED.studies = [MAIZE_PROJECT_STUDY]
        MAIZE_WATERING_FACTOR_UNWATERED.factor_type = MAIZE_WATERING_TYPE
        MAIZE_WATERING_FACTOR_UNWATERED.studies = [MAIZE_PROJECT_STUDY]

        BARLEY_FUNGAL_EXPOSURE_FACTOR_PLUS.factor_type = BARLEY_FUNGAL_EXPOSURE_TYPE
        BARLEY_FUNGAL_EXPOSURE_FACTOR_PLUS.studies = [BARLEY_PROJECT_STUDY]
        BARLEY_FUNGAL_EXPOSURE_FACTOR_MINUS.factor_type = BARLEY_FUNGAL_EXPOSURE_TYPE
        BARLEY_FUNGAL_EXPOSURE_FACTOR_MINUS.studies = [BARLEY_PROJECT_STUDY]

        session.add_all(
            [
                BARLEY_FUNGAL_EXPOSURE_FACTOR_MINUS,
                BARLEY_FUNGAL_EXPOSURE_FACTOR_PLUS,
                BARLEY_FUNGAL_EXPOSURE_TYPE,
                BARLEY_ZN_EXPOSURE_FACTOR_0,
                BARLEY_ZN_EXPOSURE_FACTOR_10,
                BARLEY_ZN_EXPOSURE_FACTOR_40,
                BARLEY_ZN_EXPOSURE_FACTOR_90,
                BARLEY_ZN_EXPOSURE_TYPE,
                MAIZE_WATERING_FACTOR_UNWATERED,
                MAIZE_WATERING_FACTOR_WATERED,
                MAIZE_WATERING_TYPE,
            ]
        )

        # Setup facility
        APPN_GREENHOUSE.facility_type = GREENHOUSE_TYPE
        APPN_GREENHOUSE.institution = APPN
        INRAE_FIELD.facility_type = FIELD_CONDITION_TYPE
        INRAE_FIELD.institution = INRAE
        session.add_all([APPN_GREENHOUSE, FIELD_CONDITION_TYPE, GREENHOUSE_TYPE, INRAE_FIELD])

        # Set up experiment
        MAIZE_EXPERIMENT.experiment_type = MAIZE_EXPERIMENT_TYPE
        MAIZE_EXPERIMENT.staffs = [JOHN_DOE]
        MAIZE_EXPERIMENT.facilities = [INRAE_FIELD]
        MAIZE_EXPERIMENT.study = MAIZE_PROJECT_STUDY
        BARLEY_EXPERIMENT.experiment_type = BARLEY_EXPERIMENT_TYPE
        BARLEY_EXPERIMENT.staffs = [CHRIS_B, STEP_W]
        BARLEY_EXPERIMENT.facilities = [APPN_GREENHOUSE]
        BARLEY_EXPERIMENT.study = BARLEY_PROJECT_STUDY
        session.add_all([MAIZE_EXPERIMENT, MAIZE_EXPERIMENT_TYPE, BARLEY_EXPERIMENT, BARLEY_EXPERIMENT_TYPE])

        # Setup biological material
        ZEA_MAYS_MATERIAL.organism = ZEA_MAYS_REFERENCE
        ZEA_MAYS_MATERIAL.studies = [MAIZE_PROJECT_STUDY]
        HORDEUM_MATERIAL.organism = HORDEUM_REFERENCE
        HORDEUM_MATERIAL.studies = [BARLEY_PROJECT_STUDY]

        session.add_all(
            [
                HORDEUM_MATERIAL,
                HORDEUM_REFERENCE,
                ZEA_MAYS_MATERIAL,
                ZEA_MAYS_REFERENCE,
            ]
        )

        # Setup observed variable
        ANTHESIS_VARIABLE.trait_reference = ANTHESIS_TRAIT
        ANTHESIS_VARIABLE.studies = [MAIZE_PROJECT_STUDY]
        ANTHESIS_VARIABLE.method = DAY_TO_ANTHESIS_METHOD
        ANTHESIS_VARIABLE.unit = DEGREE_DAY_UNIT
        REPRODUCTIVE_GROWTH_TIME_VARIABLE.trait_reference = REPRODUCTIVE_GROWTH_TIME_TRAIT
        REPRODUCTIVE_GROWTH_TIME_VARIABLE.studies = [MAIZE_PROJECT_STUDY]
        REPRODUCTIVE_GROWTH_TIME_VARIABLE.method = DAY_TO_ANTHESIS_METHOD
        REPRODUCTIVE_GROWTH_TIME_VARIABLE.unit = DEGREE_DAY_UNIT
        PROJECTED_SHOOT_AREA_VARIABLE.trait_reference = PROJECTED_SHOOT_AREA_TRAIT
        PROJECTED_SHOOT_AREA_VARIABLE.studies = [BARLEY_PROJECT_STUDY]
        PROJECTED_SHOOT_AREA_VARIABLE.method = PROJECTED_SHOOT_AREA_METHOD
        PROJECTED_SHOOT_AREA_VARIABLE.unit = KILO_PIXEL_UNIT
        ZN_CONCENTRATION_VARIABLE.trait_reference = ZN_CONCENTRATION_TRAIT
        ZN_CONCENTRATION_VARIABLE.studies = [BARLEY_PROJECT_STUDY]
        ZN_CONCENTRATION_VARIABLE.method = ZN_CONCENTRATION_METHOD
        ZN_CONCENTRATION_VARIABLE.unit = MICROGRAM_UNIT

        session.add_all(
            [
                ANTHESIS_TRAIT,
                ANTHESIS_VARIABLE,
                PROJECTED_SHOOT_AREA_TRAIT,
                PROJECTED_SHOOT_AREA_VARIABLE,
                REPRODUCTIVE_GROWTH_TIME_TRAIT,
                REPRODUCTIVE_GROWTH_TIME_VARIABLE,
                ZN_CONCENTRATION_TRAIT,
                ZN_CONCENTRATION_VARIABLE,
            ]
        )

        # Setup observation unit
        PLOT_894.observation_unit_type = PLOT_TYPE
        PLOT_894.studies = [MAIZE_PROJECT_STUDY]
        PLOT_894.facility = INRAE_FIELD
        PLOT_894.biological_material = ZEA_MAYS_MATERIAL
        PLOT_894.experimental_factors = [MAIZE_WATERING_FACTOR_WATERED]

        PLANT_061439.observation_unit_type = PLANT_TYPE
        PLANT_061439.studies = [BARLEY_PROJECT_STUDY]
        PLANT_061439.facility = APPN_GREENHOUSE
        PLANT_061439.biological_material = HORDEUM_MATERIAL
        PLANT_061439.experimental_factors = [BARLEY_ZN_EXPOSURE_FACTOR_90, BARLEY_FUNGAL_EXPOSURE_FACTOR_PLUS]

        PLANT_061440.observation_unit_type = PLANT_TYPE
        PLANT_061440.studies = [BARLEY_PROJECT_STUDY]
        PLANT_061440.facility = APPN_GREENHOUSE
        PLANT_061440.biological_material = HORDEUM_MATERIAL
        PLANT_061440.experimental_factors = [BARLEY_ZN_EXPOSURE_FACTOR_0, BARLEY_FUNGAL_EXPOSURE_FACTOR_PLUS]

        session.add_all([PLANT_061439, PLANT_061440, PLANT_TYPE, PLOT_894, PLOT_TYPE])

        # Add event
        FERTILIZING_EVENT.event_type = FERTILIZING_TYPE
        FERTILIZING_EVENT.studies = [MAIZE_PROJECT_STUDY]
        FERTILIZING_EVENT.observation_units = [PLOT_894]
        PLANTING_EVENT.event_type = PLANT_TYPE
        PLANTING_EVENT.studies = [MAIZE_PROJECT_STUDY]
        PLANTING_EVENT.observation_units = [PLOT_894]
        WATERING_EVENT.event_type = WATERING_TYPE
        WATERING_EVENT.studies = [BARLEY_PROJECT_STUDY]
        WATERING_EVENT.observation_units = [PLANT_061439, PLANT_061440]
        session.add_all(
            [FERTILIZING_EVENT, FERTILIZING_TYPE, WATERING_EVENT, WATERING_TYPE, PLANTING_EVENT, PLANTING_TYPE]
        )

        # Add sample
        CEA_BE00034067.plant_anatomical_entity = PO_0025161
        CEA_BE00034067.observation_unit = PLOT_894
        CEA_BE00034067.plant_structural_development_stage = PO_0025094
        LEAFDISC_061439.plant_anatomical_entity = PO_0006001
        LEAFDISC_061439.observation_unit = PLANT_061439
        LEAFDISC_061439.plant_structural_development_stage = PO_0007010
        LEAFDISC_061440.plant_anatomical_entity = PO_0006001
        LEAFDISC_061440.observation_unit = PLANT_061440
        LEAFDISC_061440.plant_structural_development_stage = PO_0007010

        session.add_all(
            [
                PO_0006001,
                PO_0007010,
                PO_0025094,
                PO_0025161,
                CEA_BE00034067,
                LEAFDISC_061440,
                LEAFDISC_061439,
            ]
        )
        await session.commit()

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(async_main())
