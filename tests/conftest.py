import pytest
import codecs
import pathlib
import yaml
import psycopg2
import requests
import xmlschema
from oereb_server.scripts import create_config

@pytest.fixture(scope="module")
def config():
    # create_config muss ausgeführt werden,
    # damit oereb_server.yml existiert.
    create_config.run_create_config()
    with codecs.open(r"oereb_server.yml", "r", "utf-8") as cf:
        return yaml.load(cf, Loader=yaml.FullLoader)

@pytest.fixture(scope="module")
def version():
    with codecs.open(r"src/oereb_server/__init__.py") as vf:
        for line in vf.read().splitlines():
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
        else:
            raise RuntimeError("Unable to find version string.")


@pytest.fixture(scope="module")
def app_schema_name(config):
    return config['oereb_server']['app_schema']['name']

@pytest.fixture(scope="module")
def db_connection_string(config):
    return config['oereb_server']['app_schema']['db_connection']

@pytest.fixture(scope="module")
def largest_area_parcel(db_connection_string, app_schema_name):
    with psycopg2.connect(db_connection_string) as conn:
        with conn.cursor() as cur:
            sql = "SELECT egrid FROM %s.real_estate order by land_registry_area desc limit 1" % (app_schema_name)
            cur.execute(sql)
            return cur.fetchone()[0]

@pytest.fixture(scope="module")
def complex_area_parcel(db_connection_string, app_schema_name):
    with psycopg2.connect(db_connection_string) as conn:
        with conn.cursor() as cur:
            sql = 'SELECT egrid FROM %s.real_estate order by st_npoints("limit") desc limit 1' % (app_schema_name)
            cur.execute(sql)
            return cur.fetchone()[0]

@pytest.fixture(scope="module")
def parcel_building_right(db_connection_string, app_schema_name):
    with psycopg2.connect(db_connection_string) as conn:
        with conn.cursor() as cur:
            sql = "select egrid from %s.real_estate re where re.type='SelbstRecht.Baurecht' and re.land_registry_area > 0 order by land_registry_area asc limit 1" % (app_schema_name)
            cur.execute(sql)
            return cur.fetchone()[0]

@pytest.fixture(scope="module")
def parcel_source_right(db_connection_string, app_schema_name):
    with psycopg2.connect(db_connection_string) as conn:
        with conn.cursor() as cur:
            sql = "select egrid from %s.real_estate re where re.type='SelbstRecht.Quellenrecht' and re.land_registry_area > 0 order by land_registry_area asc limit 1" % (app_schema_name)
            cur.execute(sql)
            return cur.fetchone()[0]

@pytest.fixture(scope="module")
def parcel_concession_right(db_connection_string, app_schema_name):
    with psycopg2.connect(db_connection_string) as conn:
        with conn.cursor() as cur:
            sql = "select egrid from %s.real_estate re where re.type='SelbstRecht.Konzessionsrecht' and re.land_registry_area > 0 order by land_registry_area asc limit 1" % (app_schema_name)
            cur.execute(sql)
            return cur.fetchone()[0]

@pytest.fixture(scope="module")
def running_server_instance(environment):
    server = "http://localhost:6543"
    if environment == 'test':
        server = 'https://www.oereb2-test.apps.be.ch'
    elif environment == 'prod':
        server = 'https://www.oereb2.apps.be.ch'
    return server

@pytest.fixture(scope="module")
def egrid_without_plr():
    return "CH934641351251"

@pytest.fixture(scope="module")
def egrid_with_some_plr():
    return "CH173510804618"

@pytest.fixture(scope="module")
def egrid_large_geometries_error():
    return "CH173515254641"    

@pytest.fixture(scope="module")
def number_of_municipalities(db_connection_string, app_schema_name):
    with psycopg2.connect(db_connection_string) as conn:
        with conn.cursor() as cur:
            sql = 'select count(*) from %s.municipality' % (app_schema_name)
            cur.execute(sql)
            return cur.fetchone()[0]

@pytest.fixture(scope="module")
def number_of_topics_config(db_connection_string, app_schema_name):
    with psycopg2.connect(db_connection_string) as conn:
        with conn.cursor() as cur:
            sql = 'select count(*) from %s.theme' % (app_schema_name)
            cur.execute(sql)
            return cur.fetchone()[0]

@pytest.fixture(scope="module")
def random_egrids(db_connection_string, app_schema_name):
    with psycopg2.connect(db_connection_string) as conn:
        with conn.cursor() as cur:
            sql = 'SELECT egrid from %s.real_estate ORDER BY RANDOM() LIMIT 10' % (app_schema_name)
            cur.execute(sql)
            return [egrid[0] for egrid in cur.fetchall()]

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev", help="Eines von dev, test, prod", choices=['dev', 'test', 'prod'])

@pytest.fixture(scope="module")
def environment(pytestconfig):
    return pytestconfig.getoption("--env")

@pytest.fixture(scope="module")
def egrids_for_concurrent_error():
    return ('CH594607413563', 'CH804335484602')

@pytest.fixture(scope="module")
def complex_extract_parcel():
    return 'CH643546232754'

@pytest.fixture(scope='module')
def cors_header_name():
    return "access-control-allow-origin"

@pytest.fixture(scope='session')
def schema_for_validation(tmp_path_factory):
    # dieses XML-Schema muss lokal gespeichert sein.
    # Wenn nicht, gibt es beim Import in xmlschema
    # einen Fehler. Grund: unklar.
    xmldsig_url = "http://www.w3.org/TR/xmldsig-core/xmldsig-core-schema.xsd"
    res = requests.get(xmldsig_url, timeout=30)
    temp_xmldsig_file = tmp_path_factory.mktemp("xmldsig") / "xmldsig-core-schema.xsd"
    with temp_xmldsig_file.open("w", encoding='utf-8') as f:
        f.write(res.text)
    sources = [
        "http://models.interlis.ch/refhb24/geometry.xsd",
        temp_xmldsig_file,
        "http://schemas.geo.admin.ch/V_D/OeREB/2.0/Extract.xsd",
        "http://schemas.geo.admin.ch/V_D/OeREB/2.0/ExtractData.xsd"
    ]
    schema = xmlschema.XMLSchema11(sources)
    return schema

@pytest.fixture(scope='module')
def egrid_gz_old():
    return "CH724797463501"

@pytest.fixture(scope='module')
def nbident_number_gz_new():
    return ('BE0200000065', 'GZN32-01')

@pytest.fixture(scope='module')
def egrid_blu_old():
    return "CH458946813550"
