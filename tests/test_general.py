import requests

def test_server_root(running_server_instance):
    res = requests.get(running_server_instance)
    assert res.status_code == 404

def test_invalid_url(running_server_instance):
    res = requests.get(running_server_instance + "/irgendwas/irgendwo")
    assert res.status_code == 404

def test_config_valid(config):
    schema_name = config['oereb_server']['app_schema']['name']
    assert schema_name == "oereb_server"

def test_debugtoolbar(running_server_instance):
    debugtoolbar_url = running_server_instance + "/_debug_toolbar/"
    res = requests.get(debugtoolbar_url)
    assert res.status_code == 404

def test_woredirect(running_server_instance, egrid_with_some_plr):
    url = running_server_instance + "/wo_redirect?egrid=%s&lang=de" % (egrid_with_some_plr)
    res = requests.get(url)
    assert res.status_code == 404