from importlib_metadata import version
import requests
import xml.etree.ElementTree as ET
import pytest

def test_versions_json_number_of_versions(running_server_instance):
    url = running_server_instance + "/versions/json"
    res = requests.get(url)
    res_json = res.json()
    number_of_versions_json = len(res_json['GetVersionsResponse']['supportedVersion'])
    assert res.status_code == 200
    assert number_of_versions_json == 1

def test_versions_json_version_number(running_server_instance):
    url = running_server_instance + "/versions/json"
    res = requests.get(url)
    res_json = res.json()
    version_number = res_json['GetVersionsResponse']['supportedVersion'][0]['version']
    assert res.status_code == 200
    assert version_number == 'extract-2.0'

def test_versions_xml_number_of_versions(running_server_instance):
    url = running_server_instance + "/versions/xml"
    res = requests.get(url)
    xml_root = ET.fromstring(res.text)
    number_of_versions_xml = len(xml_root.findall("{http://schemas.geo.admin.ch/V_D/OeREB/1.0/Versioning}supportedVersion"))
    assert res.status_code == 200
    assert number_of_versions_xml == 1

def test_versions_xml_version_number(running_server_instance):
    url = running_server_instance + "/versions/xml"
    res = requests.get(url)
    xml_root = ET.fromstring(res.text)
    spVer = xml_root.findall("{http://schemas.geo.admin.ch/V_D/OeREB/1.0/Versioning}supportedVersion")[0]
    version = spVer.findall("{http://schemas.geo.admin.ch/V_D/OeREB/1.0/Versioning}version")[0]
    assert res.status_code == 200
    assert version.text == 'extract-2.0'

def test_versions_implicit(running_server_instance):
    url = running_server_instance + "/versions"
    res = requests.get(url)
    assert res.status_code == 404
