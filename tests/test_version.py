import requests

def test_version_correct(running_server_instance, version):
    url = running_server_instance + "/version"
    res = requests.get(url)
    assert res.status_code == 200
    assert res.json()['version'] == version