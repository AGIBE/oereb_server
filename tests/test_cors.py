import requests

###############
# EXTRACT
###############    

def test_cors_extract_json(running_server_instance, egrid_with_some_plr, cors_header_name):
    extract_url = running_server_instance + "/extract/reduced/json/" + egrid_with_some_plr
    response = requests.get(extract_url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'    

def test_cors_extract_xml(running_server_instance, egrid_with_some_plr, cors_header_name):
    extract_url = running_server_instance + "/extract/reduced/xml/" + egrid_with_some_plr
    response = requests.get(extract_url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'    

def test_cors_extract_pdf(running_server_instance, egrid_with_some_plr, cors_header_name):
    extract_url = running_server_instance + "/extract/reduced/pdf/" + egrid_with_some_plr
    response = requests.get(extract_url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'        

###############
# CAPABILITIES
###############    

def test_cors_capabilities_json(running_server_instance, cors_header_name):
    capabilities_url = running_server_instance + "/capabilities/json"
    response = requests.get(capabilities_url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

def test_cors_capabilities_xml(running_server_instance, cors_header_name):
    capabilities_url = running_server_instance + "/capabilities/xml"
    response = requests.get(capabilities_url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

def test_cors_capabilities(running_server_instance, cors_header_name):
    capabilities_url = running_server_instance + "/capabilities"
    response = requests.get(capabilities_url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'   

###############
# VERSION
###############    

def test_version(running_server_instance, cors_header_name):
    version_url = running_server_instance + "/version"
    response = requests.get(version_url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

###############
# VERSIONS
###############    

def test_cors_versions_json(running_server_instance, cors_header_name):
    capabilities_url = running_server_instance + "/versions/json"
    response = requests.get(capabilities_url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

def test_cors_versions_xml(running_server_instance, cors_header_name):
    capabilities_url = running_server_instance + "/versions/xml"
    response = requests.get(capabilities_url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

def test_cors_versions(running_server_instance, cors_header_name):
    capabilities_url = running_server_instance + "/versions"
    response = requests.get(capabilities_url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'
    
#############
# GETEGRID XY
#############
def test_getegrid_valid_xy_single_json_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/json/?XY=2600000,1200000"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

def test_getegrid_invalid_xy_single_json_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/json/?XY=0,0"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

def test_getegrid_valid_xy_multiple_json_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/json/?XY=2599175.1,1199196.2"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

def test_getegrid_valid_xy_single_xml_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/xml/?XY=2600000,1200000"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

def test_getegrid_invalid_xy_single_xml_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/xml/?XY=0,0"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

def test_getegrid_valid_xy_multiple_xml_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/xml/?XY=2599175.1,1199196.2"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

###############
# GETEGRID GNSS
###############
def test_getegrid_valid_gnss_single_json_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/json/?GNSS=46.95108,7.43863"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

def test_getegrid_invalid_gnss_single_json_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/json/?GNSS=0,0"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

def test_getegrid_valid_gnss_multiple_json_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/json/?GNSS=46.94387,7.42781"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

def test_getegrid_valid_gnss_single_xml_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/xml/?GNSS=46.95108,7.43863"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

def test_getegrid_invalid_gnss_single_xml_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/xml/?GNSS=0,0"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

def test_getegrid_valid_gnss_multiple_xml_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/xml/?GNSS=46.94387,7.42781"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

##################
# GETEGRID IDENTDN
##################
def test_getegrid_valid_identdn_json_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/json/BE0200000043/698"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

def test_getegrid_invalid_identdn_json_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/json/0/0"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

def test_getegrid_valid_identdn_xml_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/xml/BE0200000043/698"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

def test_getegrid_invalid_identdn_xml_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/xml/0/0"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

##################
# GETEGRID ADDRESS
##################
def test_getegrid_valid_address_json_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/json/3013/Reiterstrasse/11"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

def test_getegrid_invalid_address_json_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/json/666/somestreet/666"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

def test_getegrid_valid_address_xml_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/xml/3013/Reiterstrasse/11"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'

def test_getegrid_invalid_address_xml_cors(running_server_instance, cors_header_name):
    url = running_server_instance + "/getegrid/json/666/somestreet/666"
    response = requests.get(url)
    assert cors_header_name in response.headers.keys()
    assert response.headers[cors_header_name] == '*'     
   