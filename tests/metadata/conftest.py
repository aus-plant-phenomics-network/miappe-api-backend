from pathlib import Path

import pytest

DATA = Path(__file__).parent / "data"


@pytest.fixture(params=[
    "10.5555/67890",
    "10.1093/ajae/aaq063",
    "10.1371/journal.pgen.1001111",
    "10.37044/osf.io/ekhdw",
    "10.37044/osf.io/eKhDw",
    "10.1371/journal.pone.0071377"
])
def valid_doi(request):
    return request.param


@pytest.fixture(params=[
    "10.555/67890",
    "10/osf.io/ekhdw",
])
def invalid_doi(request):
    return request.param


@pytest.fixture(params=[
    "VN",
    "US",
    "GB",
    "AU",
    "CA",
    "FR"
])
def valid_country_alpha2(request):
    return request.param


@pytest.fixture(params=[
    "AUS",
    "UK",
])
def invalid_country_alpha2(request):
    return request.param


@pytest.fixture(params=[
    "Australia",
    "Ukraine",
    "Tunisia",
    "Thailand"
])
def valid_country_name(request):
    return request.param


@pytest.fixture(params=[
    "Australian",
    "Australai"
])
def invalid_country_name(request):
    return request.param


@pytest.fixture(params=[
    "testuser@example.com",
    "john.doe123@testmail.org",
    "alice.smith@mailinator.com",
    "support@company.net",
    "info+test@emailservice.com",
])
def valid_email(request):
    return request.param


@pytest.fixture(params=[
    "user@.com",
    "@example.com",
    "user@com",
    "user@example@com",
    "user@example,com",
    "user@.123",
    "user@example_test.com",
])
def invalid_email(request):
    return request.param


@pytest.fixture(params=[
    "123",
    "+123",
    "-123",
    "123 m",
    "+123 m",
    "-123 m",
    "123.0 m",
    "+123.0 m",
    "-123.0 m",
    ".9",
    "+.9",
    "-.9",
    "0.9",
    "+0.9",
    "-0.9",
    ".9 m",
    "+.9 m",
    "-.9 m",
    "0.9 m",
    "+0.9 m",
    "-0.9 m",
    "0.9m"
])
def valid_numeric_meter(request):
    return request.param


@pytest.fixture(params=[
    "0.1-0.9",
    "0.1-0.9 m",
    "0.9mm",
    "0.9 ft",
    "0.9m0.9"
])
def invalid_numeric_meter(request):
    return request.param


@pytest.fixture(params=[
    "-33.8688",
    "151.2093",
    "40.7128",
    "-74.0060",
    "35.6895",
    "139.6917",
    "-22.9068",
    "-43.1729",
    "-33.9258",
    "18.4232"
])
def valid_latlong(request):
    return request.param


@pytest.fixture(params=[
    "abc",
    "40.123.12"
    "35.6895'N"
])
def invalid_latlong(request):
    return request.param


@pytest.fixture(params=[
    "file123.txt",
    "important_document.doc",
    "my_script.sh",
    "valid file.csv",
    "data - file.csv",
    "image - 001.j",
    "peg",
    "user_profile.txt",
    "config.ini",
    "README.md",
    "directory_name",
    "archive_2022.tar.gz",
])
def valid_filename(request):
    return request.param


@pytest.fixture(params=[
    "file & 123.",
    "image - 001 /.jpeg",
    "config *.ini",
    "README??.md",
])
def invalid_filename(request):
    return request.param


@pytest.fixture(params=[
    "https://www.example.com",
    "http://subdomain.example.org/path/to/resource",
    "http://192.168.1.1",
    "https://example.co.uk",
    "https://api.example.com/v1/users?id=123",
    "http://localhost:8080",
    "https://www.example.com/path?query=value",
])
def valid_url(request):
    return request.param


@pytest.fixture(params=[
    "htp://example.com",
    "ftp://user:password@host:21/path",
    "http:/example.com",
    "http://@example.com",
    "http://example.com:80:8080",
    "http://example.com/ space",
    "http://example..com",
])
def invalid_url(request):
    return request.param


@pytest.fixture(params=[
    ("latitude:+2.341", {"latitude": "+2.341"}),
    ("latitude:+2.341; row:4", {"latitude": "+2.341", "row": "4"}),
    ("latitude:+2.341; row:4 ; X:3; Y:6; Xm:35; Ym:65; block:1; plot:894", {
        "latitude": "+2.341", "row": "4", "X": "3", "Y": "6", "Xm": "35", "Ym": "65", "block": "1", "plot": "894"
    })
])
def valid_kv(request):
    return request.param


@pytest.fixture(params=[
    "latitude,+2.324",
    "latitude32314; row:4"
])
def invalid_kv(request):
    return request.param


@pytest.fixture(params=[
    "block>rep>plot"
])
def valid_hierarchy(request):
    return request.param


@pytest.fixture(params=[
    "block"
])
def invalid_hierarchy(request):
    return request.param


@pytest.fixture(params=[
    ("study_1; study_2", (1, None)),
    ("study_1; study_2; study_3", (1, None)),
    (None, (0, 1)),
    ("", (0, 1)),
    ("plot:894", (0, 1)),
    ("Planting, Fertilizing", (1, 1)),
    ("Planting, Fertilizing", (0, 1)),
    ("CO_715:0000007\nCO_715:0000011", (0, 1)),
    ("Sowing using seed drill\nFertilizer application: Ammonium nitrate at 3 kg/m2", (0, 1)),
    ("2006-09-27T10:23:21+00:00;2006-10-27; 2006-11-13; 2016-11-21", (1, None)),
    ("2006-09-27T10:23:21+00:00;2006-10-27; 2006-11-13; 2016-11-21", (2, None)),
    ("2006-09-27T10:23:21+00:00;2006-10-27; 2006-11-13", (2, None)),
])
def valid_value_count(request):
    return request.param


@pytest.fixture(params=[
    ("2006-09-27T10:23:21+00:00;2006-10-27; 2006-11-13; 2016-11-21", (0, 1)),
    ("plot:894; plot:123", (0, 1)),
    (None, (1, None)),
    ("", (1, None)),
    (None, (1, 1)),
    ("", (1, 1)),
    ("Planting, Fertilizing", (2, 2)),
    ("2006-09-27T10:23:21+00:00;2006-10-27; 2006-11-13; 2016-11-21", (2, 2)),
    ("2006-09-27T10:23:21+00:00,2006-10-27, 2006-11-13, 2016-11-21", (2, None)),
])
def invalid_value_count(request):
    return request.param


def miappe_example_default():
    return DATA / "test_example.xlsx"
