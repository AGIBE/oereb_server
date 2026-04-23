import pytest
import requests

def test_legend_topic_all_codes_de(running_server_instance, topic_codes):
    for topic_code in topic_codes:
        url = f"{running_server_instance}/legend_topic?code={topic_code}&lang=de"
        res = requests.get(url)
        # Es gibt nicht für jeden Topic-Code ein Legenden-File
        assert res.status_code in [200, 404]
        assert res.history[0].status_code == 303

def test_legend_topic_all_codes_fr(running_server_instance, topic_codes):
    for topic_code in topic_codes:
        url = f"{running_server_instance}/legend_topic?code={topic_code}&lang=fr"
        res = requests.get(url)
        # Es gibt nicht für jeden Topic-Code ein Legenden-File
        assert res.status_code in [200, 404]
        assert res.history[0].status_code == 303

@pytest.mark.parametrize("invalid_codes", ["ch.BEE.Gewaesserschutzbereiche", "chBEGewaesserschutzbereiche", '(O:/:OIUKZJMFG)'])
def test_legend_topic_invalid_codes_de(running_server_instance, invalid_codes):
    for topic_code in invalid_codes:
        url = f"{running_server_instance}/legend_topic?code={topic_code}&lang=de"
        res = requests.get(url)
        # Es gibt nicht für jeden Topic-Code ein Legenden-File
        assert res.status_code == 400

@pytest.mark.parametrize("invalid_codes", ["ch.BEE.Gewaesserschutzbereiche", "chBEGewaesserschutzbereiche", '(O:/:OIUKZJMFG)'])
def test_legend_topic_invalid_codes_fr(running_server_instance, invalid_codes):
    for topic_code in invalid_codes:
        url = f"{running_server_instance}/legend_topic?code={topic_code}&lang=fr"
        res = requests.get(url)
        assert res.status_code == 400

@pytest.mark.parametrize("invalid_languages", ['EN', 'ger', 'fra', 'alks*GEFéLJàHJéTZ'])
def test_legend_topic_invalid_languages(running_server_instance, invalid_languages):
    for language in invalid_languages:
        url = f"{running_server_instance}/legend_topic?code=ch.BelasteteStandorte&lang={language}"
        res = requests.get(url)
        assert res.status_code == 400
