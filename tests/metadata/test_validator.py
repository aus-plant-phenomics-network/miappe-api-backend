import pytest

from src.metadata.validator import _validate_doi, _validate_country, _validate_email, _validate_numeric, \
    _validate_lat_long, _validate_filename, _validate_url, _validate_key_value_list, _validate_hierarchy


def test_validate_valid_doi(valid_doi):
    assert valid_doi == _validate_doi(valid_doi)


def test_invalid_doi(invalid_doi):
    with pytest.raises(ValueError):
        _validate_doi(invalid_doi)


def test_validate_country_alpha2(valid_country_alpha2):
    assert valid_country_alpha2 == _validate_country(valid_country_alpha2)


def test_invalid_country_alpha2(invalid_country_alpha2):
    with pytest.raises(ValueError):
        _validate_country(invalid_country_alpha2)


def test_validate_country_name(valid_country_name):
    assert valid_country_name == _validate_country(valid_country_name)


def test_invalid_country_name(invalid_country_name):
    with pytest.raises(ValueError):
        _validate_country(invalid_country_name)


def test_valid_email(valid_email):
    assert valid_email == _validate_email(valid_email)


def test_invalid_email(invalid_email):
    with pytest.raises(ValueError):
        _validate_email(invalid_email)


def test_valid_numeric(valid_numeric_meter):
    assert valid_numeric_meter == _validate_numeric(valid_numeric_meter)


def test_invalid_numeric(invalid_numeric_meter):
    with pytest.raises(ValueError):
        _validate_numeric(invalid_numeric_meter)


def test_valid_latlong(valid_latlong):
    assert valid_latlong == _validate_lat_long(valid_latlong)


def test_invalid_latlong(invalid_latlong):
    with pytest.raises(ValueError):
        _validate_lat_long(invalid_latlong)


def test_valid_filename(valid_filename):
    assert valid_filename == _validate_filename(valid_filename)


def test_invalid_filename(invalid_filename):
    with pytest.raises(ValueError):
        _validate_filename(invalid_filename)


def test_valid_url(valid_url):
    assert valid_url == _validate_url(valid_url)


def test_invalid_url(invalid_url):
    with pytest.raises(ValueError):
        _validate_url(invalid_url)


def test_valid_kv(valid_kv):
    assert valid_kv[1] == _validate_key_value_list(valid_kv[0])


def test_invalid_kv(invalid_kv):
    with pytest.raises(ValueError):
        _validate_key_value_list(invalid_kv)


def test_hierarchy(valid_hierarchy):
    assert valid_hierarchy == _validate_hierarchy(valid_hierarchy)


def test_invalid_hierarchy(invalid_hierarchy):
    with pytest.raises(ValueError):
        _validate_hierarchy(invalid_hierarchy)
