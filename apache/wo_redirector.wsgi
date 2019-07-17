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

def wo_redirect(request):
    egrid = get_parameter_value(['egrid', 'EGRID', 'Egrid'], request)
    language = get_parameter_value(['lang','LANG','Lang'], request)
    base_url = request.host_url
    allowed_urls = ['https://www.oereb-test.apps.be.ch', 'https://www.oereb.apps.be.ch', 'http://localhost:6543']
    
    if egrid is not None and language is not None and base_url in allowed_urls:

        extract_query_string = '/extract/reduced/pdf/%s?LANG=%s' % (egrid, language)
        extract_url = base_url + extract_query_string
        return HTTPFound(location=extract_url)
    else:
        return HTTPNotFound()

with Configurator() as config:
    config.add_route('wo_redirector', '/')
    config.add_view(wo_redirect, route_name='wo_redirector')
    application = config.make_wsgi_app()