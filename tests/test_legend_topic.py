import time
import pytest
import requests


def test_legend_topic_all_codes_de(running_server_instance: str, topic_codes: list, subtests):
    for topic_code in topic_codes:
        with subtests.test(topic=topic_code):
            url = f"{running_server_instance}/legend_topic?code={topic_code}&lang=de"
            res = requests.get(url)
            time.sleep(0.5)
            # Es gibt nicht für jeden Topic-Code ein Legenden-File
            assert res.status_code in [200, 404]
            assert res.history[0].status_code == 303


def test_legend_topic_all_codes_fr(running_server_instance, topic_codes, subtests):
    for topic_code in topic_codes:
        with subtests.test(topic=topic_code):
            url = f"{running_server_instance}/legend_topic?code={topic_code}&lang=fr"
            res = requests.get(url)
            time.sleep(0.5)
            # Es gibt nicht für jeden Topic-Code ein Legenden-File
            assert res.status_code in [200, 404]
            assert res.history[0].status_code == 303


@pytest.mark.parametrize(
    "invalid_code",
    [
        "ch.BEE.Gewaesserschutzbereiche",
        "chBEGewaesserschutzbereiche",
        "(O:/:OIUKZJMFG)",
    ],
)
def test_legend_topic_invalid_codes_de(running_server_instance, invalid_code):
    url = f"{running_server_instance}/legend_topic?code={invalid_code}&lang=de"
    res = requests.get(url)
    time.sleep(0.5)
    # Es gibt nicht für jeden Topic-Code ein Legenden-File
    assert res.status_code == 400


@pytest.mark.parametrize(
    "invalid_code",
    [
        "ch.BEE.Gewaesserschutzbereiche",
        "chBEGewaesserschutzbereiche",
        "(O:/:OIUKZJMFG)",
    ],
)
def test_legend_topic_invalid_codes_fr(running_server_instance, invalid_code):
    url = f"{running_server_instance}/legend_topic?code={invalid_code}&lang=fr"
    res = requests.get(url)
    time.sleep(0.5)
    assert res.status_code == 400


@pytest.mark.parametrize("invalid_language", ["EN", "ger", "fra", "alks*GEFéLJàHJéTZ"])
def test_legend_topic_invalid_languages(running_server_instance, invalid_language):
    url = f"{running_server_instance}/legend_topic?code=ch.BelasteteStandorte&lang={invalid_language}"
    res = requests.get(url)
    time.sleep(0.5)
    assert res.status_code == 400
