import jsonschema
import requests
import xml.etree.ElementTree as ET


def test_capabilities_json_topics(running_server_instance, number_of_topics_config):
    url = running_server_instance + "/capabilities/json"
    res = requests.get(url)
    res_json = res.json()
    number_of_topics_json = len(res_json["GetCapabilitiesResponse"]["topic"])
    assert number_of_topics_json == number_of_topics_config


def test_capabilities_json_municipalities(
    running_server_instance, number_of_municipalities
):
    url = running_server_instance + "/capabilities/json"
    res = requests.get(url)
    res_json = res.json()
    number_of_municipalities_json = len(
        res_json["GetCapabilitiesResponse"]["municipality"]
    )
    assert number_of_municipalities_json == number_of_municipalities


def test_capabilities_json_flavour(running_server_instance):
    url = running_server_instance + "/capabilities/json"
    res = requests.get(url)
    res_json = res.json()
    flavour = res_json["GetCapabilitiesResponse"]["flavour"]
    assert len(flavour) == 1
    assert flavour[0].lower() == "reduced"


def test_capabilities_json_language(running_server_instance):
    url = running_server_instance + "/capabilities/json"
    res = requests.get(url)
    res_json = res.json()
    language = res_json["GetCapabilitiesResponse"]["language"]
    assert len(language) == 2
    assert language[0].lower() == "de"
    assert language[1].lower() == "fr"


def test_capabilities_json_CRS(running_server_instance):
    url = running_server_instance + "/capabilities/json"
    res = requests.get(url)
    res_json = res.json()
    crs = res_json["GetCapabilitiesResponse"]["crs"]
    assert len(crs) == 1
    assert crs[0].lower() == "epsg:2056"


def test_capabilities_json_status_code(running_server_instance):
    url = running_server_instance + "/capabilities/json"
    res = requests.get(url)
    assert res.status_code == 200


def test_capabilities_json_status_content_type(running_server_instance):
    url = running_server_instance + "/capabilities/json"
    res = requests.get(url)
    assert res.headers["Content-Type"].lower().startswith("application/json")


def test_capabilities_json_valid(running_server_instance):
    url = running_server_instance + "/capabilities/json"
    res = requests.get(url)
    res_json = res.json()
    json_schema = requests.get(
        "http://schemas.geo.admin.ch/V_D/OeREB/2.0/extract.json"
    ).json()
    resolver = jsonschema.RefResolver(
        base_uri="http://schemas.geo.admin.ch/V_D/OeREB/2.0/", referrer=json_schema
    )
    try:
        jsonschema.validate(instance=res_json, schema=json_schema, resolver=resolver)
    except jsonschema.ValidationError:
        assert False


def test_capabilities_xml_topics(running_server_instance, number_of_topics_config):
    url = running_server_instance + "/capabilities/xml"
    res = requests.get(url)
    xml_root = ET.fromstring(res.text)
    number_of_topics_xml = len(
        xml_root.findall("{http://schemas.geo.admin.ch/V_D/OeREB/2.0/Extract}topic")
    )
    assert number_of_topics_xml == number_of_topics_config


def test_capabilities_xml_municipality(
    running_server_instance, number_of_municipalities
):
    url = running_server_instance + "/capabilities/xml"
    res = requests.get(url)
    xml_root = ET.fromstring(res.text)
    number_of_municipalities_xml = len(
        xml_root.findall(
            "{http://schemas.geo.admin.ch/V_D/OeREB/2.0/Extract}municipality"
        )
    )
    assert number_of_municipalities_xml == number_of_municipalities


def test_capabilities_xml_flavour(running_server_instance):
    url = running_server_instance + "/capabilities/xml"
    res = requests.get(url)
    xml_root = ET.fromstring(res.text)
    flavour = xml_root.findall(
        "{http://schemas.geo.admin.ch/V_D/OeREB/2.0/Extract}flavour"
    )
    assert len(flavour) == 1
    assert flavour[0].text.lower() == "reduced"


def test_capabilities_language_flavour(running_server_instance):
    url = running_server_instance + "/capabilities/xml"
    res = requests.get(url)
    xml_root = ET.fromstring(res.text)
    languages = xml_root.findall(
        "{http://schemas.geo.admin.ch/V_D/OeREB/2.0/Extract}language"
    )
    assert len(languages) == 2
    assert languages[0].text.lower() == "de"
    assert languages[1].text.lower() == "fr"


def test_capabilities_xml_CRS(running_server_instance):
    url = running_server_instance + "/capabilities/xml"
    res = requests.get(url)
    xml_root = ET.fromstring(res.text)
    crs = xml_root.findall("{http://schemas.geo.admin.ch/V_D/OeREB/2.0/Extract}crs")
    assert len(crs) == 1
    assert crs[0].text.lower() == "epsg:2056"


def test_capabilities_xml_status_code(running_server_instance):
    url = running_server_instance + "/capabilities/xml"
    res = requests.get(url)
    assert res.status_code == 200


def test_capabilities_xml_status_content_type(running_server_instance):
    url = running_server_instance + "/capabilities/xml"
    res = requests.get(url)
    assert res.headers["Content-Type"].lower().startswith("application/xml")


def test_capabilities_xml_valid(running_server_instance, schema_for_validation):
    url = running_server_instance + "/capabilities/xml"
    res = requests.get(url)
    xml = res.text
    assert schema_for_validation.is_valid(xml)


def test_capabilities_xml_implicit(running_server_instance):
    url = running_server_instance + "/capabilities"
    res = requests.get(url)
    assert res.status_code == 404
