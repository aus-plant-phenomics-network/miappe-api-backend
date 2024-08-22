from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyPlugin
from litestar.openapi import OpenAPIConfig

from src.helpers import create_db_config, provide_transaction
from src.router import (
    BiologicalMaterialController,
    DataFileController,
    DeviceController,
    EnvironmentController,
    EventController,
    ExperimentalFactorController,
    ExperimentController,
    FacilityController,
    InstitutionController,
    InvestigationController,
    MethodController,
    ObservationUnitController,
    ObservedVariableController,
    SampleController,
    SPARQLController,
    StaffController,
    StudyController,
    UnitController,
    VocabularyController,
)

db_config = create_db_config("db.sqlite")
cors_config = CORSConfig(allow_origins=["*"])
app = Litestar(
    [
        DeviceController,
        VocabularyController,
        MethodController,
        UnitController,
        BiologicalMaterialController,
        DataFileController,
        EnvironmentController,
        EventController,
        ExperimentController,
        ExperimentalFactorController,
        FacilityController,
        InvestigationController,
        InstitutionController,
        ObservedVariableController,
        ObservationUnitController,
        SampleController,
        StudyController,
        StaffController,
        SPARQLController,
    ],
    dependencies={"transaction": provide_transaction},
    plugins=[SQLAlchemyPlugin(db_config)],
    cors_config=cors_config,
    openapi_config=OpenAPIConfig(title="miappe_schema", version="1.0.0"),
)
