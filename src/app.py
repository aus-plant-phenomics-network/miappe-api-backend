from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyPlugin

from src.helpers import create_db_config, provide_transaction
from src.router import *

db_config = create_db_config("db.sqlite")

app = Litestar(
    [
        DeviceController,
        VocabularyController,
        MethodController,
        UnitController,
        VariableController,
        BaseController,
        GenericController,
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
        StaffController
    ],
    dependencies={"transaction": provide_transaction},
    plugins=[SQLAlchemyPlugin(db_config)],
)
