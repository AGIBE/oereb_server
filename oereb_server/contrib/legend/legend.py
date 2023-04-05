# -*- coding: utf-8 -*-
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPSeeOther, HTTPBadRequest
from pyramid_oereb.contrib.stats.decorators import log_response

def get_parameter_value(possible_parameter_names, request):

    value = None

    for possible_parameter_name in possible_parameter_names:
        if request.GET.__contains__(possible_parameter_name):
            value = request.GET.get(possible_parameter_name)

    return value

@view_config(route_name='legend', decorator=log_response)
def legend(request):
    # Parameter mode (oereb oder oerebpruef; Default: oereb)
    mode = get_parameter_value(['mode', 'MODE', 'Mode'], request)
    if mode:
        if mode.lower() not in ['oereb', 'oerebpruef']:
            mode = 'oereb'
    else:
        mode = 'oereb'

    # Parameter bfsnr (Zahl zwischen 100 und 999)
    bfsnr = get_parameter_value(['bfsnr', 'BFSNR', 'Bfsnr'], request)
    if bfsnr:
        if bfsnr.lower().isdigit():
            if not (int(bfsnr) >= 100 and int(bfsnr) < 1000):
                return HTTPBadRequest(detail="Parameter bfsnr ungültig.")    
        else:
            return HTTPBadRequest(detail="Parameter bfsnr ungültig.")
    else:
        return HTTPBadRequest(detail="Parameter bfsnr ungültig.")
    
    # Parameter lang (de oder fr; Default: de)
    language = get_parameter_value(['lang','LANG','Lang'], request)
    if language:
        if language.lower() not in ['de', 'fr']:
            language = 'de'
    else:
        language = 'de'

    # Die Gemeinde-Legenden gibt es auf der Test-Stufe nicht. Daher
    # kann immer auf die produktive URL umgeleitet werden.        
    legend_url = "https://oerebfiles.apps.be.ch/legenden/gemeinden/{}/{}_{}.html".format(mode, bfsnr, language)
    return HTTPSeeOther(location=legend_url)