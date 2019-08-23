from waitress import serve
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound

def get_parameter_value(possible_parameter_names, request):

    value = None

    for possible_parameter_name in possible_parameter_names:
        if request.GET.__contains__(possible_parameter_name):
            value = request.GET.get(possible_parameter_name)

    return value

def wo_redirector(request):
    egrid = get_parameter_value(['egrid', 'EGRID', 'Egrid'], request)
    language = get_parameter_value(['lang','LANG','Lang'], request)
    base_url = 'https://www.oereb.apps.be.ch'
    if 'a4pu' in request.host_url:
        base_url = 'https://www.oereb-test.apps.be.ch'
    
    if egrid is not None and language is not None:

        extract_query_string = '/extract/reduced/pdf/%s?LANG=%s' % (egrid, language)
        extract_url = base_url + extract_query_string
        return HTTPFound(location=extract_url)
    else:
        return HTTPNotFound()

with Configurator() as config:
    config.add_route('wo_redirector', '/')
    config.add_view(wo_redirector, route_name='wo_redirector')
    application = config.make_wsgi_app()