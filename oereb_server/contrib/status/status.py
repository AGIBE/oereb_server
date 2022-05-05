# -*- coding: utf-8 -*-
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPOk
from pyramid.httpexceptions import HTTPServiceUnavailable
from pyramid_oereb import Config, database_adapter
import json
import requests
from oereb_server import __version__

def health_check_db():
    params = Config.get_real_estate_config().get('source').get('params')
    session = database_adapter.get_session(params.get('db_connection'))
    try:
        session.execute('SELECT 1')
        return True
    except Exception:
        return False

def health_check_print():
    print_config = Config.get('print', {})
    print_url = print_config['base_url']
    capabilities_url = print_url + '/capabilities.json'
    try:
        requests.head(capabilities_url, timeout=0.1)
        return True
    except Exception:
        return False

@view_config(route_name='status')
def status(request):
    db_status = health_check_db()
    print_status = health_check_print()
    result_dict = {
        'Is the database running?': db_status,
        'Is the print service running?': print_status,
        'Version oereb_server':  __version__
    }
    if print_status and db_status:
        return HTTPOk(body=json.dumps(result_dict), content_type='application/json', charset='UTF-8')
    else:
        return HTTPServiceUnavailable(detail=result_dict)