import enum
from functools import lru_cache
from typing import Annotated, Type, Any, Callable

import pandas as pd
from pydantic import BaseModel, create_model, Field
from pydantic.functional_validators import AfterValidator

from miappe.metadata.helpers import FORMAT_MAPPING, CARDINALITY_MAPPING, _validate_value_count, validation_sheets, \
    MODEL_PATH

# Type def
VALIDATION_ENUMS = enum.Enum('Validation_Items', validation_sheets)

# MAPPING
TITLE = "MIAPPE Check list"
DEFINITION = "Definition"
EXAMPLE = "Example"
FORMAT = "Format"
CARDINALITY = "Cardinality"


## Spreadsheet validator
@lru_cache(maxsize=100)
def _read_sheet_schema(
        sheet_type: VALIDATION_ENUMS) -> None | pd.DataFrame:
    """
    TODO: raise exception for this method
    Read schema tsv file. Schema is obtained from splitting sub-categories in MIAPPE_Checklist-Data-Model-vx.x.tsv.
    Each sub category tsv file contains the following columns:
        - MIAPPE Check List - validation fields - i.e event id, latitude, longitude
        - Definition - definition for the corresponding field
        - Example - example for the corresponding field
        - Format - expected data type.
        - Cardinality - expected number of user provided items

    :param sheet_type:  validation sub category - e.g. Event, Investigation, Observation Unit, Observed Variable etc
    :return: pd.DataFrame of the schema
    """
    try:
        return pd.read_csv(MODEL_PATH / f"{sheet_type}_model.tsv", sep='\t')
    except Exception as e:
        print(e)
        return None


def _create_count_validator(
        min_count: int = 0,
        max_count: int | None = None,
        sep: str = ";") -> Callable:
    def validate_value_count(value: Any = ...) -> Any:
        return _validate_value_count(value, sep, min_count, max_count)

    return validate_value_count


def _create_type_annotation(
        definition: str,
        example: str,
        format_t: str,
        cardinality: str,
) -> tuple[Type[Annotated], Any]:
    """
    Create pydantic compatible annotation for type checking and validation.
    Field information is to be extracted from MIAPPE_Checklist-Data-Mode and used to create
    annotation. The following actions are performed:
    - Look up python type based on format. If the schema type requires extra-validations, a corresponding
    validator will be provided. - i.e. if format is DOI, a validator to validate DOI syntax will be provided.
    - Create a count validator based on cardinality. This validator is created for every field, and will check when
    split by a separator, the resulting list will match the required cardinality.
    - Set field alias to be the title

    :param title: field title - snake-cased lowered field title
    :param definition: field definition - provided in field schema
    :param example: field example value - provided in field schema
    :param format_t: field format - provided in field schema
    :param cardinality: field cardinality - provided in field schema
    :return: field annotation of typing_extra.Annotation type
    """
    json_schema_extra = {
        'definition': definition,
        'example': example,
        'format': format_t,
        'cardinality': cardinality
    }
    base_type, validator = FORMAT_MAPPING[format_t.strip()]
    is_required, min_count, max_count = CARDINALITY_MAPPING[cardinality.split(" ")[0]]
    count_validator = _create_count_validator(min_count, max_count)
    default_value = Field(...) if is_required else None

    field = Field(
        default=default_value,  # Set to Field(...) to annotate the field being required
        json_schema_extra=json_schema_extra
    )  # Add extra json schema info)
    if validator:  # If the field requires extra validator, other than count validator
        return Annotated[base_type, AfterValidator(validator), AfterValidator(count_validator), field], default_value
    return Annotated[base_type, AfterValidator(count_validator), field], default_value


@lru_cache(100)
def create_sheet_validator(sheet_type: VALIDATION_ENUMS) -> Type[BaseModel]:
    """
    Create a pydantic BaseModel subclass based on sheet type/category.
    This is a function that dynamically generates classes that are a sub-class
    of pydantic BaseModel. The notable change is fields are lowered and have spaces
    replaced with "_" for ease of indexing. For instance, "Study unique ID" is converted
    to "study_unique_id". However, "Study unique ID" is still accepted for validation

    :param sheet_type: category -i.e Investigation, Study, Person, Sample, etc
    :return: BaseModel subclass
    """
    schema = _read_sheet_schema(sheet_type)
    field_definition = {}
    for i in range(len(schema)):
        canonical_title = schema.loc[i, TITLE].lower().replace(" ", "_").replace("\n","")
        field_definition[canonical_title] = _create_type_annotation(
            schema.loc[i, DEFINITION].strip(),
            schema.loc[i, EXAMPLE].strip(),
            schema.loc[i, FORMAT].strip(),
            schema.loc[i, CARDINALITY].strip(),
        )
    return create_model(
        __model_name=sheet_type,
        **field_definition
    )
