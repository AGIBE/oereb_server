import pytest
import requests

def test_largest_area_extract_json(running_server_instance, largest_area_parcel):
    extract_url = running_server_instance + "/extract/json/?egrid=" + largest_area_parcel
    res = requests.get(extract_url)
    assert res.status_code == 200
    assert 'GetExtractByIdResponse' in res.json().keys()

def test_largest_area_extract_pdf(running_server_instance, largest_area_parcel):
    extract_url = running_server_instance + "/extract/pdf/?egrid=" + largest_area_parcel
    res = requests.get(extract_url)
    assert res.status_code == 200

def test_parcel_without_plr_json(running_server_instance, egrid_without_plr):
    extract_url = running_server_instance + "/extract/json/?egrid=" + egrid_without_plr
    res = requests.get(extract_url)
    assert res.status_code == 200
    assert len(res.json()['GetExtractByIdResponse']['extract']['ConcernedTheme']) == 0

def test_complex_parcel_json(running_server_instance, complex_area_parcel):
    extract_url = running_server_instance + "/extract/json/?egrid=" + complex_area_parcel
    res = requests.get(extract_url)
    assert res.status_code == 200
    assert 'GetExtractByIdResponse' in res.json().keys()

def test_complex_parcel_pdf(running_server_instance, complex_area_parcel):
    extract_url = running_server_instance + "/extract/pdf/?egrid=" + complex_area_parcel
    res = requests.get(extract_url)
    assert res.status_code == 200

def test_complex_extract_json(running_server_instance, complex_extract_parcel):
    extract_url = running_server_instance + "/extract/json/?egrid=" + complex_extract_parcel
    res = requests.get(extract_url)
    assert res.status_code == 200
    assert 'GetExtractByIdResponse' in res.json().keys()

def test_complex_extract_pdf(running_server_instance, complex_extract_parcel):
    extract_url = running_server_instance + "/extract/pdf/?egrid=" + complex_extract_parcel
    res = requests.get(extract_url)
    assert res.status_code == 200

def test_large_geometry_error_extract_pdf(running_server_instance, egrid_large_geometries_error):
    # Gewisse Auszüge übergeben mapfish_print ein riesiges JSON wegen der Geometrie
    # Wenn das JSON zu gross ist, stürzt mapfish_print ab (#6930)
    extract_url = running_server_instance + "/extract/pdf/?egrid=" + egrid_large_geometries_error
    extract_url_getspec = extract_url + "?getspec=true"
    res = requests.get(extract_url)
    res_getspec = requests.get(extract_url_getspec)
    assert res.status_code == 200
    assert len(res_getspec.text)/1024/1024 < 1

def test_invalid_egrid(running_server_instance):
    extract_url = running_server_instance + "/extract/json/?egrid=666"
    res = requests.get(extract_url)
    assert res.status_code == 204

def test_extract_pdf_url_scheme(running_server_instance, egrid_with_some_plr):
    # oereb_server übergibt im JSON die URL auf sich selber.
    # Da oereb_server hinter einem Reverse Proxy läuft, weiss
    # er aber nichts von https und nimmt immer "nur" http.
    # Diese URL wird in oereb_server fix auf https gestellt.
    # Und zwar im Startup-Script mit dem Parameter url_scheme.
    extract_url = running_server_instance + "/extract/pdf/?egrid=" + egrid_with_some_plr + "&getspec=true"
    res = requests.get(extract_url)
    json = res.json()
    url_logo = json['attributes']['CantonalLogoRef']
    assert url_logo.lower().startswith('https://')


def test_random_egrids(running_server_instance, random_egrids):
    for egrid in random_egrids:
        extract_url_json = running_server_instance + "/extract/json/?egrid=" + egrid
        extract_url_pdf = running_server_instance + "/extract/pdf/?egrid=" + egrid
        res_json = requests.get(extract_url_json)
        res_pdf = requests.get(extract_url_pdf)
        assert res_json.status_code == 200
        assert res_pdf.status_code == 200

def test_extract_url_valid_egrid(running_server_instance, egrid_with_some_plr):
    extract_url = running_server_instance + "/extract/url/?egrid=" + egrid_with_some_plr
    res = requests.get(extract_url)
    assert res.status_code == 200
    assert res.history[0].status_code == 303

def test_extract_url_invalid_egrid(running_server_instance):
    extract_url = running_server_instance + "/extract/url/?egrid=666"
    res = requests.get(extract_url)
    assert res.status_code == 204

def test_extract_building_right(running_server_instance, parcel_building_right):
    extract_url = running_server_instance + "/extract/json/?egrid=" + parcel_building_right
    res = requests.get(extract_url)
    json = res.json()
    real_estate_type = json['GetExtractByIdResponse']['extract']['RealEstate']['Type']['Text'][0]['Text']
    assert res.status_code == 200
    assert real_estate_type == 'Baurecht'

def test_extract_sources_right(running_server_instance, parcel_source_right):
    extract_url = running_server_instance + "/extract/json/?egrid=" + parcel_source_right
    res = requests.get(extract_url)
    json = res.json()
    real_estate_type = json['GetExtractByIdResponse']['extract']['RealEstate']['Type']['Text'][0]['Text']
    assert res.status_code == 200
    assert real_estate_type == 'Quellenrecht'

def test_extract_concession_right(running_server_instance, parcel_concession_right):
    extract_url = running_server_instance + "/extract/json/?egrid=" + parcel_concession_right
    res = requests.get(extract_url)
    json = res.json()
    real_estate_type = json['GetExtractByIdResponse']['extract']['RealEstate']['Type']['Text'][0]['Text']
    assert res.status_code == 200
    assert real_estate_type == 'Konzessionsrecht'

def test_extract_xml_valid_schema(running_server_instance, egrid_with_some_plr, schema_for_validation):
    extract_url = running_server_instance + "/extract/xml/?egrid=" + egrid_with_some_plr
    res = requests.get(extract_url)
    xml = res.text
    assert schema_for_validation.is_valid(xml) == True

def test_extract_gz_new(running_server_instance, egrid_gz_old):
    extract_url = running_server_instance + "/extract/json/?egrid=" + egrid_gz_old
    res = requests.get(extract_url)
    assert res.status_code == 200

def test_extract_gz_old(running_server_instance, nbident_number_gz_new):
    nbident = nbident_number_gz_new[0]
    number = nbident_number_gz_new[1]
    extract_url = f"{running_server_instance}/extract/json/?identdn={nbident}&number={number}"
    res = requests.get(extract_url)
    json = res.json()
    extract_number = json['GetExtractByIdResponse']['extract']['RealEstate']['Number']
    assert res.status_code == 200
    assert extract_number.startswith("GZN")

@pytest.mark.skip(reason="Im Moment gibt es keine laufenden Baulandumlegungen.")
def test_extract_blu_new():
    pass

def test_extract_blu_old(running_server_instance, egrid_blu_old):
    extract_url = running_server_instance + "/extract/json/?egrid=" + egrid_blu_old
    res = requests.get(extract_url)
    assert res.status_code == 200
