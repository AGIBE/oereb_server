import requests

def test_legend_correct(running_server_instance):
    url = running_server_instance + "/legend?mode=oereb&bfsnr=351&lang=fr"
    res = requests.get(url)
    assert res.status_code == 200
    assert res.history[0].status_code == 303
    assert '/oereb/' in res.history[0].headers['Location']

def test_legend_invalid_bfsnr(running_server_instance):
    url = running_server_instance + "/legend?mode=oereb&bfsnr=3511&lang=fr"
    res = requests.get(url)
    assert res.status_code == 400

def test_legend_missing_bfsnr(running_server_instance):
    url = running_server_instance + "/legend?mode=oereb&lang=fr"
    res = requests.get(url)
    assert res.status_code == 400

def test_legend_missing_mode(running_server_instance):
    url = running_server_instance + "/legend?lang=fr&bfsnr=351"
    res = requests.get(url)
    assert res.status_code == 200
    assert res.history[0].status_code == 303

def test_legend_missing_lang(running_server_instance):
    url = running_server_instance + "/legend?mode=oereb&bfsnr=351"
    res = requests.get(url)
    assert res.status_code == 200
    assert res.history[0].status_code == 303

def test_legend_missing_lang_mode(running_server_instance):
    url = running_server_instance + "/legend?bfsnr=351"
    res = requests.get(url)
    assert res.status_code == 200
    assert res.history[0].status_code == 303
