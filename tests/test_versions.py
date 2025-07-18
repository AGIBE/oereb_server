import jsonschema
import requests
import xml.etree.ElementTree as ET
import xmlschema

def test_versions_json_number_of_versions(running_server_instance):
    url = running_server_instance + "/versions/json"
    res = requests.get(url)
    res_json = res.json()
    number_of_versions_json = len(res_json['GetVersionsResponse']['supportedVersion'])
    assert number_of_versions_json == 1

def test_versions_json_version_number(running_server_instance):
    url = running_server_instance + "/versions/json"
    res = requests.get(url)
    res_json = res.json()
    version_number = res_json['GetVersionsResponse']['supportedVersion'][0]['version']
    assert version_number == 'extract-2.0'

def test_versions_json_content_type(running_server_instance):
    url = running_server_instance + "/versions/json"
    res = requests.get(url)
    assert res.headers['Content-Type'].lower().startswith("application/json")

def test_versions_json_status_code(running_server_instance):
    url = running_server_instance + "/versions/json"
    res = requests.get(url)
    assert res.status_code == 200

def test_versions_json_valid(running_server_instance):
    json_schema = requests.get("http://schemas.geo.admin.ch/V_D/OeREB/2.0/versioning.json").json()
    url = running_server_instance + "/versions/json"
    res = requests.get(url)
    json_res = res.json()
    try:
        jsonschema.validate(instance=json_res, schema=json_schema)
    except jsonschema.ValidationError:
        assert False

def test_versions_xml_number_of_versions(running_server_instance):
    url = running_server_instance + "/versions/xml"
    res = requests.get(url)
    xml_root = ET.fromstring(res.text)
    number_of_versions_xml = len(xml_root.findall("{http://schemas.geo.admin.ch/V_D/OeREB/1.0/Versioning}supportedVersion"))
    assert number_of_versions_xml == 1

def test_versions_xml_version_number(running_server_instance):
    url = running_server_instance + "/versions/xml"
    res = requests.get(url)
    xml_root = ET.fromstring(res.text)
    spVer = xml_root.findall("{http://schemas.geo.admin.ch/V_D/OeREB/1.0/Versioning}supportedVersion")[0]
    version = spVer.findall("{http://schemas.geo.admin.ch/V_D/OeREB/1.0/Versioning}version")[0]
    assert version.text == 'extract-2.0'

def test_versions_xml_content_type(running_server_instance):
    url = running_server_instance + "/versions/xml"
    res = requests.get(url)
    assert res.headers['Content-Type'].lower().startswith("application/xml")

def test_versions_xml_status_code(running_server_instance):
    url = running_server_instance + "/versions/xml"
    res = requests.get(url)
    assert res.status_code == 200

def test_versions_xml_valid(running_server_instance):
    url = running_server_instance + "/versions/xml"
    res = requests.get(url)
    xml = res.text
    schema = xmlschema.XMLSchema("http://schemas.geo.admin.ch/V_D/OeREB/2.0/Versioning.xsd")
    assert schema.is_valid(xml)

def test_versions_implicit(running_server_instance):
    url = running_server_instance + "/versions"
    res = requests.get(url)
    assert res.status_code == 404
