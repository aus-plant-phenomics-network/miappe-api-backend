import datetime
import re
from pathlib import Path
from typing import Any, Union

import pycountry
import yaml

# Files
RESOURCE_PATH = Path(__file__).parent / 'resource'
MODEL_PATH = RESOURCE_PATH / 'model'
TEMPLATE_PATH = RESOURCE_PATH / 'template'

with open(MODEL_PATH / 'metadata.yaml', 'r') as file:
    validation_sheets = yaml.safe_load(file)['Item']

# List of REGEX
DOI_REGEX = r"""^10\.\d{4,9}\/[-._;()/:a-zA-Z0-9]+$"""  # DOI
COUNTRY_NAME = [country.name for country in pycountry.countries]  # Country Name
COUNTRY_CODE_2 = [country.alpha_2 for country in pycountry.countries]  # Country 2-letter codes
LAT_LONG_REGEX = r"^-?([0-9]{1,2}|1[0-7][0-9]|180)(\.[0-9]{1,7})?$"  # Match up to 7 digits - lat long ISO std
NUMERIC_UNIT_REGEX = r"^[-+]?\d*\.?\d+\s?m?$"  # Number with an optional 'm'
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# Define Type
NullableStr = str | None


# REGEX validators
def _validate_regex(
        input_pattern: str,
        str_input: NullableStr,
        exception_message: str) -> NullableStr:
    if str_input is None:
        return None
    pattern = re.compile(input_pattern)
    if re.fullmatch(pattern, str_input) is None:
        raise ValueError(f"Fail to validate: {str_input}. {exception_message}")
    return str_input


def _validate_country(name: str) -> str:
    if (name not in COUNTRY_NAME) and (name not in COUNTRY_CODE_2):
        raise ValueError(
            f"""Fail to validate: {name}.
            Invalid country name (ISO 3166-1 name) or 2 letter country code (ISO 3166-1 alpha 2)""")
    return name


def _validate_doi(doi: str) -> str:
    return _validate_regex(DOI_REGEX, doi, "Invalid DOI format")


def _validate_lat_long(degree: str) -> str:
    return _validate_regex(LAT_LONG_REGEX, degree, "Invalid Lat/Long Degree (ISO 6709)")


def _validate_numeric(item: str) -> str:
    return _validate_regex(NUMERIC_UNIT_REGEX, item,
                           "Invalid input, must be numeric with optional unit (m)")


def _validate_url(url: str) -> str:
    def is_valid_url(_url: str) -> bool:
        regex = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return _url is not None and regex.search(_url)

    if not (is_valid_url(url)):
        raise ValueError(f"{url}. Invalid URL")
    return url


def _validate_filename(url: str) -> str:
    def is_valid_filename(filename):
        # Define a regular expression for a valid filename
        pattern = re.compile(r'^[a-zA-Z0-9_.\- ]+$')

        # List of reserved keywords for both Unix and Windows
        reserved_keywords = ['con', 'prn', 'aux', 'nul', 'com1', 'com2', 'com3', 'com4', 'com5', 'com6', 'com7', 'com8',
                             'com9',
                             'lpt1', 'lpt2', 'lpt3', 'lpt4', 'lpt5', 'lpt6', 'lpt7', 'lpt8', 'lpt9']

        # Check if the filename matches the pattern, is not empty, and does not contain reserved keywords
        return bool(pattern.match(filename)) and len(filename) > 0 and filename.lower() not in reserved_keywords

    if not (is_valid_filename(url)):
        raise ValueError(f"{url}. Invalid filename")
    return url


def _validate_email(email: str) -> str:
    return _validate_regex(EMAIL_REGEX, email, "Invalid email address - RFC 5322")


def _validate_key_value_list(kv: str) -> dict:
    pairs = kv.split(";")
    merged_dict = {}
    for pair in pairs:
        group = pair.split(":")
        if len(group) != 2:
            raise ValueError(f"{kv}. Invalid key value list")
        merged_dict.update({group[0].strip(): group[1].strip()})
    return merged_dict


def _validate_url_filename(item: str) -> str:
    try:
        return _validate_url(item)
    except ValueError:
        try:
            return _validate_filename(item)
        except ValueError:
            raise ValueError("Invalid URL or Filename")


def _validate_url_doi(item: str) -> str:
    try:
        return _validate_url(item)
    except ValueError:
        try:
            return _validate_doi(item)
        except ValueError:
            raise ValueError("Invalid URL or DOI")


def _validate_hierarchy(item: str) -> str:
    if ">" in item:
        return item
    raise ValueError(f"{item}. Invalid Hierarchy format")


def _validate_value_count(
        value: Any = ...,
        sep: str = ";",
        min_count: int | None = None,
        max_count: int | None = None) -> Any:
    # Convert to container type
    if isinstance(value, str):
        value_ = [item for item in value.split(sep) if item.strip() != ""]
    else:
        if hasattr(value, "__len__"):
            value_ = value
        else:
            value_ = [value] if value is not None else []

    # Validate count
    length = len(value_)
    if min_count is not None:
        if length < min_count:
            raise ValueError(f"Fail cardinality constraint requirement: min count: {min_count}, length: {length}")
    if max_count is not None:
        if length > max_count:
            raise ValueError(f"Fail cardinality constraint requirement: max count: {max_count}, length: {length}")
    return value


# List of validators as regex functions
DOI_VALIDATOR = _validate_doi
COUNTRY_VALIDATOR = _validate_country
DEGREE_VALIDATOR = _validate_lat_long
NUMERIC_UNIT_VALIDATOR = _validate_numeric
NUMERIC_UNIT_OPTIONAL_VALIDATOR = _validate_numeric
URL_FILENAME_VALIDATOR = _validate_url_filename
EMAIL_VALIDATOR = _validate_email
KEY_VALUE_LIST_VALIDATOR = _validate_key_value_list
URI_DOI_VALIDATOR = _validate_url_doi
HIERARCHY_VALIDATOR = _validate_hierarchy

# Mapping from MIAPPE format to python data type - tuple of (pythonType, validator)
FORMAT_MAPPING = {
    "Free text (short)": (NullableStr, None),
    "Free text": (NullableStr, None),
    "Free text (see Appendix I)": (NullableStr, None),
    "Free text (see Appendix II)": (NullableStr, None),
    "Unique identifier": (NullableStr, None),
    "Date/Time (ISO 8601, optional time zone)": (Union[datetime.datetime, datetime.date], None),
    "Version number": (NullableStr, None),
    "DOI": (NullableStr, DOI_VALIDATOR),
    "Country name or 2-letter code (ISO 3166)": (NullableStr, COUNTRY_VALIDATOR),
    "Degrees in the decimal format (ISO 6709)": (NullableStr, DEGREE_VALIDATOR),
    "Numeric + unit abbreviation": (NullableStr, NUMERIC_UNIT_VALIDATOR),
    'Crop Ontology term (subclass of "CO_715:0000003")': (NullableStr, None),  # TODO: Add validator
    'Crop Ontology term (subclass of "CO_715:0000005")': (NullableStr, None),  # TODO: Add validator
    'Crop Ontology term (subclass of CO_715:0000006)': (NullableStr, None),  # TODO: Add validator
    "URL or File name (of gis or tabular file like csv or tsv)": (NullableStr, URL_FILENAME_VALIDATOR),
    "URL or File name": (NullableStr, URL_FILENAME_VALIDATOR),
    "List": (NullableStr, None),
    "Name": (NullableStr, None),
    "email address": (NullableStr, EMAIL_VALIDATOR),
    "Software version number": (NullableStr, None),
    "Genus name": (NullableStr, None),
    "Species name": (NullableStr, None),
    "Free text, or key-value pair list, or MCPD-compliant format": (NullableStr, None),
    "Numeric": (NullableStr, NUMERIC_UNIT_OPTIONAL_VALIDATOR),
    "Plant Environment Ontology and/or free text": (NullableStr, None),
    "Formatted text (Key:value)": (NullableStr, KEY_VALUE_LIST_VALIDATOR),
    "Plant Ontology term (subclass of PO:0009012) or BBCH scale term": (NullableStr, None),  # TODO: Add validator
    "Plant Ontology term (subclass of PO:0025131)": (NullableStr, None),  # TODO: Add validator
    "Date/Time": (Union[datetime.datetime, datetime.date], None),
    "Crop Ontology term": (NullableStr, None),
    "Term from Plant Trait Ontology, Crop Ontology, or XML Environment Ontology": (NullableStr, None),
    "URI or DOI": (NullableStr, URI_DOI_VALIDATOR),
    "Formatted text (level>level)": (NullableStr, HIERARCHY_VALIDATOR)
}

# Number of required parameters - tuple of (isRequired, minCount, maxCount)
CARDINALITY_MAPPING = {
    "0-1": (False, 0, 1),
    "0+": (False, 0, None),
    "1": (True, 1, 1),
    "1+": (True, 1, None),
    "2": (True, 2, 2),
    "2+": (True, 2, None)
}
