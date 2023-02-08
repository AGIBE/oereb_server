import requests

def test_version_correct(running_server_instance, version):
    url = running_server_instance + "/version"
    res = requests.get(url)
    assert res.json()['version'] == version

def test_version_status_code(running_server_instance):
    url = running_server_instance + "/version"
    res = requests.get(url)
    assert res.status_code == 200

def test_version_content_type(running_server_instance):
    url = running_server_instance + "/version"
    res = requests.get(url)
    assert res.headers['Content-Type'].lower() == 'application/json'
