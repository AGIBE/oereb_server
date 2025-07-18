import time
import jsonschema
import requests
import xml.etree.ElementTree as ET
import pytest

# Diese Variablen wurden explizit nicht als Fixtures
# realisiert, da es in pytest nicht möglich ist,
# Fixtures in pytest.mark.parametrize zu verwenden.
getegrid_combos_invalid = [
    "json/?EN=0,0",
    "xml/?EN=0,0",
    "json/?GNSS=0,0",
    "xml/?GNSS=0,0",
    "json/?IDENTDN=0&NUMBER=0",
    "xml/?IDENTDN=0&NUMBER=0",
    "json/?POSTALCODE=666&LOCALISATION=somestreet&NUMBER=666",
    "xml/?POSTALCODE=666&LOCALISATION=somestreet&NUMBER=666"
]

getegrid_combos_json_single = [
    "json/?EN=2600000,1200000",
    "json/?GNSS=46.95108,7.43863",
    "json/?IDENTDN=BE0200000043&NUMBER=698",
    "json/?POSTALCODE=3013&LOCALISATION=Reiterstrasse&NUMBER=11"
]

getegrid_combos_xml_single = [
    "xml/?EN=2600000,1200000",
    "xml/?GNSS=46.95108,7.43863",
    "xml/?IDENTDN=BE0200000043&NUMBER=698",
    "xml/?POSTALCODE=3013&LOCALISATION=Reiterstrasse&NUMBER=11"
]

getegrid_combos_json_multiple = [
    "json/?EN=2608774.5,1192170.6",
    "json/?GNSS=46.88060,7.55375",
    "json/?POSTALCODE=3110&LOCALISATION=Hunzigenallee&NUMBER=1"
]

getegrid_combos_xml_multiple = [
    "xml/?EN=2608774.5,1192170.6",
    "xml/?GNSS=46.88060,7.55375",
    "xml/?POSTALCODE=3110&LOCALISATION=Hunzigenallee&NUMBER=1"
]

getegrid_combos_xml_valid = getegrid_combos_xml_single + getegrid_combos_xml_multiple
getegrid_combos_json_valid = getegrid_combos_json_single + getegrid_combos_json_multiple
all_valid_getegrid_combos = getegrid_combos_xml_valid + getegrid_combos_json_valid

# Die GETEGRID-Tests müssen etwas verlangsamt werden,
# ansonsten gibt es eine Fehlermeldung vom Proxy.
# Wirkt nur bei den GETEGRID-Tests.
@pytest.fixture(autouse=True)
def slow_down_tests():
    yield
    time.sleep(0.5)

@pytest.mark.parametrize("request_params", all_valid_getegrid_combos)
def test_getegrid_status_code_valid(running_server_instance, request_params):
    url = running_server_instance + "/getegrid/" + request_params
    res = requests.get(url)
    assert res.status_code == 200

@pytest.mark.parametrize("request_params", getegrid_combos_json_single)
def test_getegrid_single_json(running_server_instance, request_params):
    url = running_server_instance + "/getegrid/" + request_params
    res = requests.get(url)
    assert len(res.json()['GetEGRIDResponse']) == 1

@pytest.mark.parametrize("request_params", getegrid_combos_xml_single)
def test_getegrid_single_xml(running_server_instance, request_params):
    url = running_server_instance + "/getegrid/" + request_params
    res = requests.get(url)
    xml_root = ET.fromstring(res.text)
    assert len(xml_root.findall("{http://schemas.geo.admin.ch/V_D/OeREB/2.0/Extract}egrid")) == 1

@pytest.mark.parametrize("request_params", getegrid_combos_json_multiple)
def test_getegrid_multiple_json(running_server_instance, request_params):
    url = running_server_instance + "/getegrid/" + request_params
    res = requests.get(url)
    assert len(res.json()['GetEGRIDResponse']) == 2

@pytest.mark.parametrize("request_params", getegrid_combos_xml_multiple)
def test_getegrid_multiple_xml(running_server_instance, request_params):
    url = running_server_instance + "/getegrid/" + request_params
    res = requests.get(url)
    xml_root = ET.fromstring(res.text)
    assert len(xml_root.findall("{http://schemas.geo.admin.ch/V_D/OeREB/2.0/Extract}egrid")) == 2

@pytest.mark.parametrize("request_params", getegrid_combos_json_valid)
def test_getegrid_json_content_type(running_server_instance, request_params):
    url = running_server_instance + "/getegrid/" + request_params
    res = requests.get(url)
    assert res.headers['Content-Type'].lower().startswith("application/json")

@pytest.mark.parametrize("request_params", getegrid_combos_xml_valid)
def test_getegrid_xml_content_type(running_server_instance, request_params):
    url = running_server_instance + "/getegrid/" + request_params
    res = requests.get(url)
    assert res.headers['Content-Type'].lower().startswith("application/xml")

@pytest.mark.parametrize("request_params", getegrid_combos_json_valid)
def test_getegrid_json_no_geometry_implicit(running_server_instance, request_params):
    url = running_server_instance + "/getegrid/" + request_params
    res = requests.get(url)
    res_json = res.json()
    with pytest.raises(KeyError):
        len(res_json['GetEGRIDResponse'][0]['limit']['coordinates'])

@pytest.mark.parametrize("request_params", getegrid_combos_xml_valid)
def test_getegrid_xml_no_geometry_implicit(running_server_instance, request_params):
    url = running_server_instance + "/getegrid/" + request_params
    res = requests.get(url)
    xml_root = ET.fromstring(res.text)
    assert len(xml_root.findall("{http://schemas.geo.admin.ch/V_D/OeREB/2.0/Extract}limit")) == 0

@pytest.mark.parametrize("request_params", getegrid_combos_json_valid)
def test_getegrid_json_no_geometry_explicit(running_server_instance, request_params):
    url = running_server_instance + "/getegrid/" + request_params + "&GEOMETRY=FALSE"
    res = requests.get(url)
    res_json = res.json()
    with pytest.raises(KeyError):
        len(res_json['GetEGRIDResponse'][0]['limit']['coordinates'])

@pytest.mark.parametrize("request_params", getegrid_combos_xml_valid)
def test_getegrid_xml_no_geometry_explicit(running_server_instance, request_params):
    url = running_server_instance + "/getegrid/" + request_params + "&GEOMETRY=FALSE"
    res = requests.get(url)
    xml_root = ET.fromstring(res.text)
    assert len(xml_root.findall("{http://schemas.geo.admin.ch/V_D/OeREB/2.0/Extract}limit")) == 0

@pytest.mark.parametrize("request_params", getegrid_combos_json_valid)
def test_getegrid_json_geometry_explicit(running_server_instance, request_params):
    url = running_server_instance + "/getegrid/" + request_params + "&GEOMETRY=TRUE"
    res = requests.get(url)
    res_json = res.json()
    assert len(res_json['GetEGRIDResponse'][0]['limit']['coordinates']) >= 1

@pytest.mark.parametrize("request_params", getegrid_combos_xml_valid)
def test_getegrid_xml_geometry_explicit(running_server_instance, request_params):
    url = running_server_instance + "/getegrid/" + request_params + "&GEOMETRY=TRUE"
    res = requests.get(url)
    xml_root = ET.fromstring(res.text)
    assert len(xml_root.findall("{http://schemas.geo.admin.ch/V_D/OeREB/2.0/Extract}limit")) >= 1

@pytest.mark.parametrize("request_params", getegrid_combos_json_valid)
def test_getegrid_json_valid(running_server_instance, request_params):
    url = running_server_instance + "/getegrid/" + request_params
    res = requests.get(url)
    res_json = res.json()
    json_schema = requests.get("http://schemas.geo.admin.ch/V_D/OeREB/2.0/extract.json").json()
    resolver = jsonschema.RefResolver(base_uri="http://schemas.geo.admin.ch/V_D/OeREB/2.0/", referrer=json_schema)
    try:
        jsonschema.validate(instance=res_json, schema=json_schema, resolver=resolver)
    except jsonschema.ValidationError:
        assert False    

@pytest.mark.parametrize("request_params", getegrid_combos_json_valid)
def test_getegrid_json_geometry_valid(running_server_instance, request_params):
    url = running_server_instance + "/getegrid/" + request_params + "&GEOMETRY=TRUE"
    res = requests.get(url)
    res_json = res.json()
    json_schema = requests.get("http://schemas.geo.admin.ch/V_D/OeREB/2.0/extract.json").json()
    resolver = jsonschema.RefResolver(base_uri="http://schemas.geo.admin.ch/V_D/OeREB/2.0/", referrer=json_schema)
    try:
        jsonschema.validate(instance=res_json, schema=json_schema, resolver=resolver)
    except jsonschema.ValidationError:
        assert False    

@pytest.mark.parametrize("request_params", getegrid_combos_xml_valid)
def test_getegrid_xml_valid(running_server_instance, request_params, schema_for_validation):
    url = running_server_instance + "/getegrid/" + request_params
    res = requests.get(url)
    xml = res.text
    assert schema_for_validation.is_valid(xml)

@pytest.mark.parametrize("request_params", getegrid_combos_xml_valid)
def test_getegrid_xml_geometry_valid(running_server_instance, request_params, schema_for_validation):
    url = running_server_instance + "/getegrid/" + request_params + "&GEOMETRY=TRUE"
    res = requests.get(url)
    xml = res.text
    assert schema_for_validation.is_valid(xml)


@pytest.mark.parametrize("request_params", getegrid_combos_invalid)
def test_getegrid_status_code_invalid(running_server_instance, request_params):
    url = running_server_instance + "/getegrid/" + request_params
    res = requests.get(url)
    assert res.status_code == 204
