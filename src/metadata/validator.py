import datetime
import re
import pycountry

# List of REGEX
DOI_REGEX = "/^10.\d{4,9}/[-._;()/:A-Z0-9]+$/i"  # DOI
COUNTRY_NAME = [country.name for country in pycountry.countries]  # Country Name
COUNTRY_CODE_2 = [country.alpha_2 for country in pycountry.countries]  # Country 2-letter codes
LAT_LONG_REGEX = "^-?([0-9]{1,2}|1[0-7][0-9]|180)(\.[0-9]{1,7})?$"  # Match up to 7 digits - lat long ISO std
NUMERIC_UNIT_REGEX = "^[-+]?\d*\.?\d+\s?m?$"  # Number with an optional 'm'
EMAIL_REGEX = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
FILENAME_REGEX = """\A(?!(?:COM[0-9]|CON|LPT[0-9]|NUL|PRN|AUX|com[0-9]|con|lpt[0-9]|nul|prn|aux)
                |\s|[\.]{2,})[^\\\/:*"?<>|]{1,254}(?<![\s\.])\z"""  # Unix + Windows Filename
URL_REGEX = """^((https?|ftp|smtp):\/\/)?(www.)?[a-z0-9]+\.[a-z]+(\/[a-zA-Z0-9#]+\/?)*$"""  # URL based on RFC
HIERARCHY_REGEX = "^[a-zA-Z0-9_]+(:[a-zA-Z0-9_]+)?(>[a-zA-Z0-9_]+(:[a-zA-Z0-9_]+)?)*$"  # str > str > str ...
KEY_VALUE_REGEX = "(?:[a-zA-Z_]\w*):[^;]+;(?:[a-zA-Z_]\w*):[^;]+;(?:[a-zA-Z_]\w*):[^;]+"


# REGEX validators
def _validate_regex(
        pattern: str,
        str_input: str,
        exception_message: str) -> str:
    if re.fullmatch(pattern, str_input) is None:
        raise ValueError(exception_message)
    return str_input


def _validate_country(name: str) -> str:
    if (name not in COUNTRY_NAME) or (name not in COUNTRY_CODE_2):
        raise ValueError("Invalid country name (ISO 3166-1 name) or 2 letter country code (ISO 3166-1 alpha 2)")
    return name


def _validate_doi(doi: str) -> str:
    return _validate_regex(DOI_REGEX, doi, "Invalid DOI format")


def _validate_lat_long(degree: str) -> str:
    return _validate_regex(LAT_LONG_REGEX, degree, "Invalid Lat/Long Degree (ISO 6709)")


def _validate_numeric(item: str) -> str:
    return _validate_regex(NUMERIC_UNIT_REGEX, item,
                           "Invalid input, must be numeric with optional unit (m)")


def _validate_url(url: str) -> str:
    return _validate_regex(URL_REGEX, url, "Invalid url")


def _validate_filename(url: str) -> str:
    return _validate_regex(FILENAME_REGEX, url, "Invalid filename")


def _validate_email(email: str) -> str:
    return _validate_regex(EMAIL_REGEX, email, "Invalid email address - RFC 5322")


def _validate_key_value_list(kv: str) -> dict:
    try:
        items = _validate_regex(KEY_VALUE_REGEX, kv, "Invalid Key Value format")
        pairs = [{item.split(":")[0]: item.split(":")[1]} for item in items.split(":")]
        merged_dict = {}
        for pair in pairs:
            merged_dict.update(pair)
        return merged_dict
    except ValueError as e:
        raise e


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
    return _validate_regex(HIERARCHY_REGEX, item, "Item must be arranged in a hierarchy format")


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
    "Free text (short)": (str, None),
    "Free text": (str, None),
    "Free text (see Appendix I)": (str, None),
    "Free text (see Appendix II)": (str, None),
    "Unique identifier": (str, None),
    "Date/Time (ISO 8601, optional time zone)": (datetime.datetime, None),
    "Version number": (str, None),
    "DOI": (str, DOI_VALIDATOR),
    "Country name or 2-letter code (ISO 3166)": (str, COUNTRY_VALIDATOR),
    "Degrees in the decimal format (ISO 6709)": (str, DEGREE_VALIDATOR),
    "Numeric + unit abbreviation": (str, NUMERIC_UNIT_VALIDATOR),
    'Crop Ontology term (subclass of "CO_715:0000003")': (str, None),  # TODO: Add validator
    'Crop Ontology term (subclass of "CO_715:0000005")': (str, None),  # TODO: Add validator
    'Crop Ontology term (subclass of CO_715:0000006)': (str, None),  # TODO: Add validator
    "URL or File name (of gis or tabular file like csv or tsv)": (str, URL_FILENAME_VALIDATOR),
    "URL or File name": (str, URL_FILENAME_VALIDATOR),
    "List": (str, None),
    "Name": (str, None),
    "email address": (str, EMAIL_VALIDATOR),
    "Software version number": (str, None),
    "Genus name": (str, None),
    "Species name": (str, None),
    "Free text, or key-value pair list, or MCPD-compliant format": (str, None),
    "Numeric": (str, NUMERIC_UNIT_OPTIONAL_VALIDATOR),
    "Plant Environment Ontology and/or free text": (str, None),
    "Formatted text (Key:value)": (str, KEY_VALUE_LIST_VALIDATOR),
    "Plant Ontology term (subclass of PO:0009012) or BBCH scale term": (str, None),  # TODO: Add validator
    "Plant Ontology term (subclass of PO:0025131)": (str, None),  # TODO: Add validator
    "Date/Time": (datetime.datetime, None),
    "Crop Ontology term": (str, None),
    "Term from Plant Trait Ontology, Crop Ontology, or XML Environment Ontology": (str, None),
    "URI or DOI": (str, URI_DOI_VALIDATOR),
    "Formatted text (level>level)": (str, HIERARCHY_VALIDATOR)
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
