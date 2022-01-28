# -*- coding: utf-8 -*-
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from pyramid.httpexceptions import HTTPOk
from pyramid_oereb.contrib.stats.decorators import log_response

def get_parameter_value(possible_parameter_names, request):

    value = None

    for possible_parameter_name in possible_parameter_names:
        if request.GET.__contains__(possible_parameter_name):
            value = request.GET.get(possible_parameter_name)

    return value

@view_config(route_name='wo_redirect', decorator=log_response)
def wo_redirect(request):
    egrid = get_parameter_value(['egrid', 'EGRID', 'Egrid'], request)
    language = get_parameter_value(['lang','LANG','Lang'], request)
    if egrid is not None and language is not None:
        extract_query_string = '/extract/pdf?egrid=%s&lang=%s' % (egrid, language)
        # request.application_url scheint das richtige zu sein. 
        # Bei /versions/json wird es auch verwendet. Scheint
        # scheme zu berücksichtigen.
        extract_url = request.application_url + extract_query_string
        return HTTPFound(location=extract_url)
    else:
        return HTTPNotFound()
