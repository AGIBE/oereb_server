import requests

###############
# EXTRACT
###############


def test_cors_extract_json(
    running_server_instance, egrid_with_some_plr, cors_header_name
):
    extract_url = running_server_instance + "/extract/json?egrid=" + egrid_with_some_plr
    response = requests.get(extract_url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 200


def test_cors_extract_xml(
    running_server_instance, egrid_with_some_plr, cors_header_name
):
    extract_url = running_server_instance + "/extract/xml?egrid=" + egrid_with_some_plr
    response = requests.get(extract_url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 200


def test_cors_extract_pdf(
    running_server_instance, egrid_with_some_plr, cors_header_name
):
    extract_url = running_server_instance + "/extract/pdf?egrid=" + egrid_with_some_plr
    response = requests.get(extract_url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 200


###############
# CAPABILITIES
###############


def test_cors_capabilities_json(running_server_instance, cors_header_name):
    capabilities_url = running_server_instance + "/capabilities/json"
    response = requests.get(capabilities_url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 200


def test_cors_capabilities_xml(running_server_instance, cors_header_name):
    capabilities_url = running_server_instance + "/capabilities/xml"
    response = requests.get(capabilities_url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 200


###############
# VERSION
###############


def test_version(running_server_instance, cors_header_name):
    version_url = running_server_instance + "/version"
    response = requests.get(version_url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 200


###############
# LEGEND
###############


def test_legend(running_server_instance, cors_header_name):
    legend_url = running_server_instance + "/legend?bfsnr=351"
    response = requests.get(legend_url)
    assert cors_header_name in response.history[0].headers.keys()
    assert response.history[0].headers[cors_header_name] == "*"
    assert response.history[0].status_code == 303


###############
# VERSIONS
###############


def test_cors_versions_json(running_server_instance, cors_header_name):
    capabilities_url = running_server_instance + "/versions/json"
    response = requests.get(capabilities_url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 200


def test_cors_versions_xml(running_server_instance, cors_header_name):
    capabilities_url = running_server_instance + "/versions/xml"
    response = requests.get(capabilities_url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 200


#############
# GETEGRID XY
#############
def test_getegrid_valid_xy_single_json_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/json/?EN=2600000,1200000"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 200


def test_getegrid_invalid_xy_single_json_cors(
    running_server_instance, cors_header_name
):
    url = running_server_instance + "/getegrid/json/?EN=0,0"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 204


def test_getegrid_valid_xy_multiple_json_cors(
    running_server_instance, cors_header_name
):
    url = running_server_instance + "/getegrid/json/?EN=2599175.1,1199196.2"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 200


def test_getegrid_valid_xy_single_xml_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/xml/?EN=2600000,1200000"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 200


def test_getegrid_invalid_xy_single_xml_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/xml/?EN=0,0"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 204


def test_getegrid_valid_xy_multiple_xml_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/xml/?EN=2599175.1,1199196.2"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 200


###############
# GETEGRID GNSS
###############
def test_getegrid_valid_gnss_single_json_cors(
    running_server_instance, cors_header_name
):
    url = running_server_instance + "/getegrid/json/?GNSS=46.95108,7.43863"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 200


def test_getegrid_invalid_gnss_single_json_cors(
    running_server_instance, cors_header_name
):
    url = running_server_instance + "/getegrid/json/?GNSS=0,0"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 204


def test_getegrid_valid_gnss_multiple_json_cors(
    running_server_instance, cors_header_name
):
    url = running_server_instance + "/getegrid/json/?GNSS=46.94387,7.42781"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 200


def test_getegrid_valid_gnss_single_xml_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/xml/?GNSS=46.95108,7.43863"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 200


def test_getegrid_invalid_gnss_single_xml_cors(
    running_server_instance, cors_header_name
):
    url = running_server_instance + "/getegrid/xml/?GNSS=0,0"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 204


def test_getegrid_valid_gnss_multiple_xml_cors(
    running_server_instance, cors_header_name
):
    url = running_server_instance + "/getegrid/xml/?GNSS=46.94387,7.42781"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 200


##################
# GETEGRID IDENTDN
##################
def test_getegrid_valid_identdn_json_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/json/?IDENTDN=BE0200000043&NUMBER=698"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 200


def test_getegrid_invalid_identdn_json_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/json/?IDENTDN=0&NUMBER=0"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 204


def test_getegrid_valid_identdn_xml_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/xml/?IDENTDN=BE0200000043&NUMBER=698"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 200


def test_getegrid_invalid_identdn_xml_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/xml/?IDENTDN=0&NUMBER=0"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 204


##################
# GETEGRID ADDRESS
##################
def test_getegrid_valid_address_json_cors(running_server_instance, cors_header_name):
    url = (
        running_server_instance
        + "/getegrid/json/?postalcode=3013&localisation=Reiterstrasse&number=11"
    )
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 200


def test_getegrid_invalid_address_json_cors(running_server_instance, cors_header_name):
    url = (
        running_server_instance
        + "/getegrid/json/?postalcode=666&localisation=somestreet&number=666"
    )
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 204


def test_getegrid_valid_address_xml_cors(running_server_instance, cors_header_name):
    url = (
        running_server_instance
        + "/getegrid/xml/?postalcode=3013&localisation=Reiterstrasse&number=11"
    )
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 200


def test_getegrid_invalid_address_xml_cors(running_server_instance, cors_header_name):
    url = (
        running_server_instance
        + "/getegrid/xml/?postalcode=666&localisation=somestreet&number=666"
    )
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == "*"
    assert response.status_code == 204
